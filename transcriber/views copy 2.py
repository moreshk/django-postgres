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
from urllib.request import urlretrieve


def chapter_to_dict(chapter):
    return {
        'summary': chapter['summary'],
        'gist': chapter['gist'],
        'headline': chapter['headline'],
        'start': chapter['start'],
        'end': chapter['end']
    }

def milliseconds_to_seconds(milliseconds):
    return milliseconds / 1000.0


def create_lessons(course, chapters):
    print("I am in create lessons")
    for index, chapter in enumerate(chapters, start=1):

        start_seconds = milliseconds_to_seconds(chapter.start)
        end_seconds = milliseconds_to_seconds(chapter.end)
        
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

        print("Trimming lesson")
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
            dialog=chapter.summary,
            headline=chapter.gist,
            start_time=start_time,
            end_time=end_time,
            video_file=video_file_url,
        )

@method_decorator(login_required, name='dispatch')
class TranscribeView(View):
    template_name = 'transcriber/transcribe.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    
        
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

        # Set auto_chapters to True in the TranscriptionConfig
        config = aai.TranscriptionConfig(auto_chapters=True)

        transcriber = aai.Transcriber(config=config)

        # transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_url)

        # Extract the transcribed text
        transcribed_text = transcript.text
        # timed_transcribed_text = transcript.export_subtitles_vtt()

        print("Completed Transcription")

        print(transcribed_text)

        # Print auto chapters
        if transcript.status == 'completed':
            for chapter in transcript.chapters:
                print(f"Chapter Start Time: {chapter.start}")
                print(f"Chapter End Time: {chapter.end}")
                print(f"Chapter Headline: {chapter.headline}")
                print(f"Chapter Gist: {chapter.gist}")
                print(f"Chapter Summary: {chapter.summary}")
        elif transcript.status == 'error':
            print(f"Transcription failed: {transcript.error}")


        logo_filename = None

        if not logo_file:
            # Extract the thumbnail URL
            ydl_opts = {'skip_download': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(youtube_url, download=False)
                thumbnail_url = info_dict['thumbnail']

            # Download the thumbnail
            logo_filename = 'thumbnail_' + timestamp + '.jpg'
            urlretrieve(thumbnail_url, logo_filename)

            # Upload the thumbnail to Azure
            with open(logo_filename, 'rb') as f:
                logo_file = ContentFile(f.read(), name=logo_filename)
                azure_filename = default_storage.save('logos/' + logo_filename, logo_file)

            # Delete the downloaded thumbnail
            os.remove(logo_filename)

            # Use the Azure filename for the logo
            logo_filename = azure_filename
        else:
            # Save the logo file to Azure
            logo_filename = default_storage.save('logos/' + logo_file.name, logo_file)


        print("Creating new course")
        # Create a new Course object
        course = Course(
            name=name,
            description=description,
            video_link=youtube_url,
            transcript=transcribed_text,
            # timed_transcripts=timed_transcribed_text,
            logo=logo_filename,
            creator=request.user,  # Set the creator to the current user
        )

        print("Created new course, now uploading the video to Azure")

                # Upload the video file to Azure
        with open(video_filename + '.' + video_ext, 'rb') as f:
            video_file = ContentFile(f.read(), name=video_filename + '.' + video_ext)
            course.video_file.save(video_filename + '.' + video_ext, video_file)

        # Delete the audio and video files
        os.remove(audio_filename + '.mp3')
        os.remove(video_filename + '.' + video_ext)

        course.save()

        print("Creating new lessons")
        create_lessons(course, transcript.chapters)
        
         # Convert chapters to dictionaries before passing to JsonResponse
        chapters_dict = [chapter_to_dict(chapter) for chapter in transcript.chapters]
        return JsonResponse(chapters_dict, safe=False)