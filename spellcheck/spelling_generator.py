import glob
import openai
import os
import requests
import uuid
from dotenv import load_dotenv
from pathlib import Path
# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Get ElevenLabs API key from environment variable
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
openai.api_key = OPENAI_API_KEY

ELEVENLABS_VOICE_STABILITY = 0.30
ELEVENLABS_VOICE_SIMILARITY = 0.75

# Choose your favorite ElevenLabs voice
ELEVENLABS_VOICE_NAME = "Raj"
# ELEVENLABS_ALL_VOICES = []

def limit_conversation_history(conversation: list, limit: int = 30) -> list:
    """Limit the size of conversation history.

    :param conversation: A list of previous user and assistant messages.
    :param limit: Number of latest messages to retain. Default is 3.
    :returns: The limited conversation history.
    :rtype: list
    """
    return conversation[-limit:]


def generate_reply(conversation: list) -> str:
    """Generate a ChatGPT response.
    :param conversation: A list of previous user and assistant messages.
    :returns: The ChatGPT response.
    :rtype: str
    """
    # print("Original conversation length:", len(conversation))
    # print("Original Conversation", conversation)
    # Limit conversation history
    conversation = limit_conversation_history(conversation)
    
    # print("Limited conversation length:", len(conversation))
    print("New Conversation", conversation)

   
    # Get the corresponding character prompt
    prompt = """You are a spelling tester bot. Your job is to test a student on their ability to spell a word correctly. 
    You will start with easy words and steadily make them more complex. Here is a sample for you to pick the words for the test. 
    Level 1 (Simple, everyday words):
Cat
Dog
Hat
Sun
Run
Cup
Bed
Sit
Pen
Top
Level 2 (Common two-syllable words):
Apple
Chair
Happy
River
Lemon
Basket
Window
Garden
Yellow
Pencil
Level 3 (Common words with common blends and digraphs):
Street
Cloud
Branch
Throat
Grass
Flight
Whisper
Chrome
Blanket
Flower
Level 4 (Three-syllable words and common prefixes/suffixes):
Chocolate
Exciting
Elephant
Universe
Dangerous
Butterfly
Remember
Beginning
Universe
Exciting
Level 5 (Common compound words and more syllables):
Basketball
Toothbrush
Raincoat
Sunflower
Pineapple
Butterflies
Earthquake
Playground
Footprint
Sandcastle
Level 6 (Words with silent letters and less common blends):
Knowledge
Wrinkle
Thumb
Gnome
Castle
Knight
Wrist
Lamb
Muscle
Honest
Level 7 (Challenging multisyllabic words):
Vocabulary
Mysterious
Competition
Spectacular
Fundamental
Literature
Navigation
Celebrate
Preparation
Captivate
Level 8 (Words with irregular spellings):
Colonel
Rhythm
Gauge
Plague
Cough
Trough
Thought
Drought
Sovereign
Scissors
Level 9 (Words from foreign languages, often used in English):
Ballet
Rendezvous
Faux pas
Entrepreneur
Bouquet
Genre
Croissant
Doppelganger
Hors d'oeuvre
Déjà vu Level 10 (Advanced vocabulary, often from technical, literary, or cultural contexts):
Idiosyncrasy
Disproportionate
Perspicacious
Saccharine
Eviscerate
Cacophony
Exsanguinate
Vicissitude
Sesquipedalian
Ineffable. 
Level 1 being the easiest and Level 10 is the hardest. 
You will start with words from level 1 and create sentences that use the word and ask the user to spell the word in question. 
For eg: Apple. An Apple fell on his head. Spell the word Apple. The user will then type in the spelling for the relevant word. 
If the spelling is correct, in the next message use a word from the higher level. 
Note that the list of words is only for guidance and you can either pick the words from the list for that level or pick another word that would fit at that level. 
Continue this till the user gets the spelling wrong. At that point mention the last level which the user got right. 
Refuse to answer any questions or comments that are not relevant to this task."""

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
                {
                    "role": "system", 
                    "content": prompt 
                }

        ] + conversation,
        temperature=1
    )
    return response["choices"][0]["message"]["content"]

def purge_audio_directory(directory_path):
    """Delete all files in a directory.
    :param directory_path: Path to the directory to purge.
    :type directory_path: str
    """
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def generate_audio(text: str) -> str:
    """Converts text to audio using ElevenLabs API and returns the relative path of the saved audio file.

    :param text: The text to convert to audio.
    :type text : str
    :returns: The relative path to the successfully saved audio file.
    :rtype: str
    """
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    AUDIO_DIR = os.path.join(BASE_DIR, "static", "audio")

    # Purge the audio directory
    purge_audio_directory(AUDIO_DIR)
    
    voice_id = "21m00Tcm4TlvDq8ikWAM"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "content-type": "application/json"
    }

    data = {
        "text": text,
        "voice_settings": {
            "stability": ELEVENLABS_VOICE_STABILITY,
            "similarity_boost": ELEVENLABS_VOICE_SIMILARITY,
        }
    }

    response = requests.post(url, json=data, headers=headers)
    
    # Generate the relative and absolute paths
    output_path_relative = os.path.join("audio", f"{uuid.uuid4()}.mp3")
    output_path_absolute = os.path.join(BASE_DIR, "static", output_path_relative)
    
    # Save the audio file
    with open(output_path_absolute, "wb") as output:
        output.write(response.content)
    
    return output_path_relative
