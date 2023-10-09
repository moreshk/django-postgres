from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .spelling_generator import generate_reply, generate_audio

@login_required
def index(request):
    response_message = None
    audio_path = None  # Initialize the variable to store the path to the generated audio
    
    if request.method == 'POST':
        if 'start_test' in request.POST:
            # Clear the session
            request.session['conversation_history'] = []  # Resetting just the conversation history
            
            initial_message = {"role": "user", "content": "Start"}
            conversation_history = [initial_message]  # Initialize the conversation_history here
            print("new convo: ", conversation_history)
            response_message = generate_reply(conversation_history)
            audio_path = generate_audio(response_message)  # Generate audio for the response
            conversation_history.append({"role": "assistant", "content": response_message})

        elif 'check_spelling' in request.POST:
            user_input = request.POST.get('text_input')
            user_message = {"role": "user", "content": user_input}
            # Get conversation history from session or initialize with an empty list
            conversation_history = request.session.get('conversation_history', [])
            conversation_history.append(user_message)
            print("continuing convo: ", conversation_history)
            response_message = generate_reply(conversation_history)
            audio_path = generate_audio(response_message)  # Generate audio for the response
            conversation_history.append({"role": "assistant", "content": response_message})

        # Save the updated conversation history to the session
        request.session['conversation_history'] = conversation_history
    else:
        # If not a POST request, retrieve the conversation history or initialize with an empty list
        conversation_history = request.session.get('conversation_history', [])

    context = {
        'response_message': response_message,
        'audio_path': audio_path  # Add the audio path to the context
    }
    return render(request, 'spellcheck/index.html', context)
