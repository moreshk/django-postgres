from dotenv import load_dotenv
import os
load_dotenv()
print(os.environ.get('ELEVENLABS_API_KEY'))  # This should print the port number