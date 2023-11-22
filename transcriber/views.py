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
            # timed_transcripts=srt_json,
            logo=logo_filename,
        )
        course.save()

        return HttpResponse(transcribed_text)