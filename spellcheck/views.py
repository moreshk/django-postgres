from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .spelling_generator import generate_reply

# Create your views here.
@login_required
def index(request):
    response_message = None
    # Get conversation history from session or initialize with an empty list
    conversation_history = request.session.get('conversation_history', [])

    if request.method == 'POST':
        if 'start_test' in request.POST:
            initial_message = {"role": "user", "content": "Start"}
            conversation_history.append(initial_message)
            response_message = generate_reply(conversation_history)
            conversation_history.append({"role": "assistant", "content": response_message})

        elif 'check_spelling' in request.POST:
            user_input = request.POST.get('text_input')
            user_message = {"role": "user", "content": user_input}
            conversation_history.append(user_message)
            response_message = generate_reply(conversation_history)
            conversation_history.append({"role": "assistant", "content": response_message})

    # Save the updated conversation history to the session
    request.session['conversation_history'] = conversation_history

    context = {
        'response_message': response_message
    }
    return render(request, 'spellcheck/index.html', context)
# def index(request):
#     response_message = None
#     conversation_history = []

#     if request.method == 'POST':
#         if 'start_test' in request.POST:
#             initial_message = [{"role": "user", "content": "Start"}]
#             response_message = generate_reply(initial_message)
#             # Add the initial message and response to the conversation history
#             conversation_history.append(initial_message[0])
#             conversation_history.append({"role": "assistant", "content": response_message})
#         elif 'check_spelling' in request.POST:
#             user_input = request.POST.get('text_input')
#             user_message = {"role": "user", "content": user_input}
#             # Add user input to the conversation history
#             conversation_history.append(user_message)
#             response_message = generate_reply(conversation_history)
#             # Add the response to the conversation history
#             conversation_history.append({"role": "assistant", "content": response_message})

#     context = {
#         'response_message': response_message
#     }
#     return render(request, 'spellcheck/index.html', context)

