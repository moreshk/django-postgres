from django.core.management.base import BaseCommand
from chatbot.models import Topic
import openai
import requests
from io import BytesIO
from django.core.files.images import ImageFile
import os

class Command(BaseCommand):
    help = 'Populate images for topics without images'

    def handle(self, *args, **options):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            self.stdout.write(self.style.ERROR('OpenAI API key not found.'))
            return

        topics_without_images = Topic.objects.filter(image__isnull=True)

        if not topics_without_images:
            self.stdout.write(self.style.WARNING('No topics without images found.'))
            return

        for topic in topics_without_images:
            prompt = f"Create an image that will work to illustrate this concept. {topic.topic}. {topic.description}. Genre: {topic.genre}. Subgenre: {topic.subgenre}. Make sure there is no text in the image and keep the images simple."
            try:
                response = openai.Image.create(
                    prompt=prompt,
                    model="dall-e-3",
                    n=1,
                    size="1024x1024"
                )
                image_url = response['data'][0]['url']
                self.stdout.write(f"Image URL: {image_url}")  # Log the image URL

                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_file = BytesIO(image_response.content)
                    topic.image.save(f"{topic.topic}.png", ImageFile(image_file), save=True)
                    topic.save()  # Explicitly save the topic instance
                    self.stdout.write(self.style.SUCCESS(f"Image saved for topic: {topic.topic}"))
                else:
                    self.stdout.write(self.style.ERROR(f"Failed to download image for topic: {topic.topic}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error generating image for topic: {topic.topic}. Error: {e}"))