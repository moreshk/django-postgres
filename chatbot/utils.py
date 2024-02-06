# chatbot/utils.py

import hashlib
import json

def generate_hash_key(user_input, history, topic_id):
    # Create a unique string from user input, history, and topic ID
    unique_string = json.dumps({
        'user_input': user_input,
        'history': history,
        'topic_id': topic_id
    }, sort_keys=True)
    # Generate a hash key
    return hashlib.sha256(unique_string.encode('utf-8')).hexdigest()


def generate_history_hash(history):
    history_string = json.dumps(history, sort_keys=True).encode('utf-8')
    return hashlib.md5(history_string).hexdigest()