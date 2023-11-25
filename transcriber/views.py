from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import yt_dlp
from moviepy.editor import AudioFileClip
import assemblyai as aai
import os
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import time
from django.core.files.base import ContentFile
from labeller.models import Course
 
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from django.http import JsonResponse
from labeller.models import Lesson
import json

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from datetime import datetime

import requests
from datetime import timedelta

import string

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def milliseconds_to_seconds(milliseconds):
    return milliseconds / 1000.0

def match_timestamps_to_segments(segments, word_timestamps):
    lessons_data = []
    last_index = 0
    for segment in segments:
        words_in_segment = preprocess_text(segment['Dialog']).split()
        start_time = None
        end_time = None
        word_index = 0
        for i in range(last_index, len(word_timestamps)):
            word_info = word_timestamps[i]
            if preprocess_text(word_info['word']) == words_in_segment[word_index]:
                if start_time is None:
                    start_time = word_info['start']
                end_time = word_info['end']
                word_index += 1
                if word_index == len(words_in_segment):
                    last_index = i + 1  # Update the last index to start the next segment
                    break
        if word_index != len(words_in_segment):
            print(f"Warning: Not all words in the segment '{segment['Dialog']}' were found in the word timestamps")
        lessons_data.append({
            'Headline': segment['Headline'],
            'Dialog': segment['Dialog'],
            'Start time': start_time,
            'End time': end_time,
        })
    return lessons_data

def create_lessons(course, lessons_data):
    print("I am in create lessons")
    for index, lesson_data in enumerate(lessons_data, start=1):
        
        start_seconds = milliseconds_to_seconds(lesson_data['Start time'])
        end_seconds = milliseconds_to_seconds(lesson_data['End time'])

        # Convert seconds to datetime.time
        start_time = (datetime.min + timedelta(seconds=start_seconds)).time()
        end_time = (datetime.min + timedelta(seconds=end_seconds)).time()

        # Generate a unique filename for the trimmed video
        trimmed_video_filename = 'trimmed_video_' + str(index) + '.mp4'

        # Download the course video file to a local path
        course_video_path = 'course_video_' + str(index) + '.mp4'
        response = requests.get(course.video_file.url, stream=True)
        with open(course_video_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Trim the video
        ffmpeg_extract_subclip(course_video_path, start_seconds, end_seconds, targetname=trimmed_video_filename)

        # Upload the trimmed video to Azure
        with open(trimmed_video_filename, 'rb') as f:
            trimmed_video_file = ContentFile(f.read(), name=trimmed_video_filename)
            video_file_url = default_storage.save(trimmed_video_filename, trimmed_video_file)

        # Delete the trimmed video file and the downloaded course video file
        os.remove(trimmed_video_filename)
        os.remove(course_video_path)

        Lesson.objects.create(
            course=course,
            step_id=index * 10,
            dialog=lesson_data['Dialog'],
            headline=lesson_data['Headline'],
            start_time=start_time,
            end_time=end_time,
            video_file=video_file_url,
        )

@method_decorator(login_required, name='dispatch')
class TranscribeView(View):
    template_name = 'transcriber/transcribe.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post_processing(self, response, word_timestamps):
    # Placeholder logic
        print("I am now building lessons")
        
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
        

        course_splitter_prompt = PromptTemplate(
            input_variables=["transcript"],
            template="""You are a course creator that uses Youtube videos as reference. 
            You will be provided a transcript of a video as input. 
            You will analyze the text and break it down into logical components of three to six sentences each so that only one concept is discussed in each of them. 
            Note that you are not modifying the text but only breaking down it into logical parts so that concepts can be explained piecemeal. 
            You will return your response as json with the following column headers, Headline and Dialog.
            Dialog would be the logically broken up transcript portion and headline would be a title that describes that portions content in brief. 

            Transcript: {transcript}
    """,
        )


        chain = LLMChain(llm=llm, prompt=course_splitter_prompt)

        inputs = {
            "transcript": response,
        }

        split_lessons = chain.run(inputs)

        print("Here are the split lessons")

        print(split_lessons)

        split_lessons = json.loads(split_lessons)
        lessons = split_lessons['data']
        print("I am now building lessons based on time stamps")

        lessons_data = match_timestamps_to_segments(lessons, word_timestamps)
        
        print("Timed split Lessons : ", lessons_data)

        return lessons_data
        
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        description = request.POST.get('description')
        youtube_url = request.POST.get('youtube_url')
        logo_file = request.FILES.get('logo')

        # Generate a unique filename for the audio file
        timestamp = str(int(time.time()))
        audio_filename = 'audio_' + timestamp
        video_filename = 'video_' + timestamp

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': audio_filename,  # use the unique filename
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        # Upload the audio file to Azure
        with open(audio_filename + '.mp3', 'rb') as f:
            default_storage.save(audio_filename + '.mp3', f)

        # Download the video
        ydl_opts = {
            'format': 'best',
            'outtmpl': video_filename + '.%(ext)s',  # use the unique filename
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            video_ext = info_dict['ext']



        # Get the URL of the uploaded audio file
        audio_url = default_storage.url(audio_filename + '.mp3')

        aai.settings.api_key = os.getenv('ASSEMBLY_AI_API_KEY')
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_url)

        # Extract the transcribed text
        transcribed_text = transcript.text
        timed_transcribed_text = transcript.export_subtitles_vtt()

        print("Completed Transcription")

        # Print word-level timestamps
        for word_info in transcript.words:
            print(f"Word: {word_info.text}, Start: {word_info.start}, End: {word_info.end}")


        logo_filename = None
        if logo_file:
            # Save the logo file to Azure
            logo_filename = default_storage.save('logos/' + logo_file.name, logo_file)

        # Create a new Course object
        course = Course(
            name=name,
            description=description,
            video_link=youtube_url,
            transcript=transcribed_text,
            timed_transcripts=timed_transcribed_text,
            logo=logo_filename,
            creator=request.user,  # Set the creator to the current user
        )

                # Upload the video file to Azure
        with open(video_filename + '.' + video_ext, 'rb') as f:
            video_file = ContentFile(f.read(), name=video_filename + '.' + video_ext)
            course.video_file.save(video_filename + '.' + video_ext, video_file)

        # Delete the audio and video files
        os.remove(audio_filename + '.mp3')
        os.remove(video_filename + '.' + video_ext)

        course.save()

        # Create a list of word-level timestamps
        word_timestamps = [
            {"word": word_info.text, "start": word_info.start, "end": word_info.end}
            for word_info in transcript.words
        ]

        # Pass the word-level timestamps to the post_processing function
        lessons_data = self.post_processing(transcribed_text, word_timestamps)

        # Create lessons
        create_lessons(course, lessons_data)
        
        return JsonResponse(lessons_data, safe=False)