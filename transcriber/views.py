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

def create_lessons(course, lessons_data):
    for index, lesson_data in enumerate(lessons_data, start=1):
        Lesson.objects.create(
            course=course,
            step_id=index * 10,
            dialog=lesson_data['Dialog'],
            headline=lesson_data['Headline'],
            start_time=lesson_data['Start time'],
            end_time=lesson_data['End time'],
        )


@method_decorator(login_required, name='dispatch')
class TranscribeView(View):
    template_name = 'transcriber/transcribe.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post_processing(self, response, srt_file):
    # Placeholder logic
        print("I am now building lessons")
        
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
        

        course_splitter_prompt = PromptTemplate(
            input_variables=["transcript"],
            template="""You are a course creator that uses Youtube videos as reference. 
            You will be provided a transcript of a video as input. 
            You will analyze the text and break it down into logical components of one to five sentences each so that only one small concept is discussed in each of them. 
            Note that you are not modifying the text but only breaking down it into small logical parts so that concepts can be explained piecemeal. 
            You will also remove text that references sponsors especially if it does not add to the overall concept that is being explained in the transcript directly. 
            You will return your response as json with the following column headers, Headline and Dialog. 

            Transcript: {transcript}
    """,
        )


        chain = LLMChain(llm=llm, prompt=course_splitter_prompt)

        inputs = {
            "transcript": response,
        }

        split_lessons = chain.run(inputs)

        print(split_lessons)

        # Now I will try to combine based on time stamps on the srt file

        print("I am now building lessons based on time stamps")
        
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
        

        timed_course_creator_prompt = PromptTemplate(
            input_variables=["input_json","srt_file"],
            template="""You are a course creators assistant. 
            You will be provided 2 inputs, a json and a srt files content with time stamps for transcribed text.
            The json has the following column headers, Headline and Dialog for the various lessons in the course.
            The srt file has the same general content from the dialog field but it has timestamps.
            The contents in the srt can have one sentence broken across multiple time frame segments.

            Your job is to create a new json by cross referencing the input json and the srt files time stamps.

            Your new json will have the following column headers, Headline, Dialog, Start time, End time.

            For eg: Headline and Dialog from the json could be 

            "Headline": "The End of the Universe",
            "Dialog": "The Universe today is happy and healthy, with exciting things going on. But at some point, the night will turn dark. Everything that once was will peacefully sleep forever. But what is the last thing that will ever happen? And when will it be? It turns out there is such a thing, and you probably haven't heard about it."

            and srt file might have 

            00:00.330 --> 00:04.186
            You. The Universe today is happy and healthy,

            00:04.298 --> 00:08.318
            with exciting things going on. But at some point, the night

            00:08.404 --> 00:11.742
            will turn dark. Everything that once was

            00:11.876 --> 00:14.430
            will peacefully sleep forever.

            00:15.090 --> 00:17.838
            But what is the last thing that will ever happen?

            00:17.924 --> 00:21.406
            And when will it be? It turns out there is such

            00:21.428 --> 00:25.030
            a thing, and you probably haven't heard about it.

            You will then return a json with the same Headline and Dialog and Start time as 00:00.330 and End time as 00:25.030

            Your inputs are:

            Input Json: {input_json}

            Srt file: {srt_file}

            Remember your new json will have the following column headers, Headline, Dialog, Start time, End time (based on the Dialogs text cross referenced against the time stamps in the srt).
            It will have multiple records in this fashion, make sure to go through all of them.

    """,
        )

        chain = LLMChain(llm=llm, prompt=timed_course_creator_prompt)

        inputs = {
            "input_json": split_lessons,
            "srt_file": srt_file,
        }

        timed_split_lessons = chain.run(inputs)

        timed_split_lessons = timed_split_lessons.replace("New Json:", "").strip()
        lessons_data = json.loads(timed_split_lessons)

        print("Timed split Lessons : ", lessons_data)

        return lessons_data
        
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        description = request.POST.get('description')
        youtube_url = request.POST.get('youtube_url')
        logo_file = request.FILES.get('logo')

        # Generate a unique filename for the audio file
        timestamp = str(int(time.time()))
        filename = 'audio_' + timestamp

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': filename,  # use the unique filename
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        # Upload the audio file to Azure
        with open(filename + '.mp3', 'rb') as f:
            default_storage.save(filename + '.mp3', f)

        # Get the URL of the uploaded audio file
        audio_url = default_storage.url(filename + '.mp3')

        aai.settings.api_key = os.getenv('ASSEMBLY_AI_API_KEY')
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_url)

        # Extract the transcribed text
        transcribed_text = transcript.text
        timed_transcribed_text = transcript.export_subtitles_vtt()

        print("Completed Transcription")
        # Delete the audio file
        os.remove(filename + '.mp3')

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
        course.save()

        # Post processing
        lessons_data = self.post_processing(transcribed_text, timed_transcribed_text)

        # Create lessons
        create_lessons(course, lessons_data['data'])

        return JsonResponse(lessons_data, safe=False)