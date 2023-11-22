import assemblyai as aai

aai.settings.api_key = "3d91e1f391bf4e15b4ed43e9831d4d77"

audio_url = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

transcriber = aai.Transcriber()

transcript = transcriber.transcribe(audio_url)
print(transcript.export_subtitles_srt())
