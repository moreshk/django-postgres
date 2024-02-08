# chatbot/management/commands/simulate_chatbot.py
from django.core.management.base import BaseCommand, CommandError
from django.test import Client
from django.contrib.auth import get_user_model
from chatbot.models import Topic
import json
import copy

User = get_user_model()

class Command(BaseCommand):
    help = 'Simulates user interactions to prepopulate the response cache for a specific topic'

    def add_arguments(self, parser):
        parser.add_argument('topic_name', type=str, help='The name of the topic to simulate')

    def handle(self, *args, **options):
        topic_name = options['topic_name']
        client = Client()

        # Create or get a test user for authentication
        user, _ = User.objects.get_or_create(email='testuser@example.com', defaults={'password': 'testpass'})
        user.set_password('testpass')
        user.save()

        # Force login with the test client
        client.force_login(user)
        self.stdout.write(self.style.SUCCESS('Test user authenticated.'))

        # Get the topic by name
        try:
            topic = Topic.objects.get(topic=topic_name)
        except Topic.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Topic '{topic_name}' does not exist."))
            return  # Exit the command if the topic does not exist

        self.stdout.write(f"Starting simulation for topic: {topic.topic}")
        self.simulate_interaction(client, topic.topic, topic.description)
    
    def simulate_interaction(self, client, topic, description, history=None):
            # Initialize history with 'start' message if it's the first interaction
            if history is None:
                history = [{'role': 'user', 'content': 'start'}]
                self.stdout.write(f"Starting simulation with initial message: {history[0]['content']}")
            else:
                self.stdout.write(f"Simulating interaction with history length: {len(history)}")

                # Set the session variables explicitly
            session = client.session
            session['topic'] = f"{topic},{description}"  # Ensure the topic is set correctly
            session.save()  # Save the session after setting the topic

            # Debug output to verify the topic in the session
            self.stdout.write(f"Session topic set to: {session.get('topic', 'No topic found')}")


            # The last message in history is the message to send
            message_to_send = history[-1]['content']
            self.stdout.write(f"Sending message: {message_to_send}")

            # Send the message
            response = client.post('/chatbot/personal-tutor/chat/', json.dumps({
                'message': message_to_send,
                'topic': f"{topic},{description}"
            }), content_type='application/json')

            # Parse the response
            data = json.loads(response.content)
            chat_response = data.get('response', '')
            self.stdout.write(f"Received response: {chat_response[:50]}...")  # Print the first 50 characters

            # Append the assistant's response to the history if it's not a duplicate
            if history[-1]['role'] != 'assistant':
                history.append({'role': 'assistant', 'content': chat_response})

            # Call the text-to-speech view to get the audio response
            self.generate_audio_response(client, chat_response)

            # Extract options from the response
            options = self.extract_options(chat_response)
            self.stdout.write(f"Extracted options: {options}")

            # If there are no options, this branch is complete
            if not options:
                self.stdout.write("No more options available, ending this branch.")
                return

            # Recursively explore each option
            for option in options:
                self.stdout.write(f"Exploring option: {option}")
                # Create a new history for the next interaction, including the user's choice
                next_history = copy.deepcopy(history) 
                next_history.append({'role': 'user', 'content': option})  # Add user's response
                # Recursively call simulate_interaction with the updated history
                self.simulate_interaction(client, topic, description, next_history)


    def generate_audio_response(self, client, text):
            # Remove options from the text before generating the audio response
            text_without_options = text.split('Options:')[0].strip()
            self.stdout.write(f"Generating audio response for text: {text_without_options[:50]}...")  # Print the first 50 characters

            response = client.post('/chatbot/text-to-speech/', json.dumps({'text': text_without_options}), content_type='application/json')
            if response.status_code == 200:
                self.stdout.write("Audio response generated successfully.")
            else:
                self.stdout.write(f"Failed to generate audio response: {response.status_code}")



    def extract_options(self, response):
        # Extract options from the chatbot's response
        if 'Options:' in response:
            options_part = response.split('Options:')[-1].strip()
            options = [option.strip() for option in options_part.split(',')]
            return options
        return []