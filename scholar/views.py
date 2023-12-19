# scholar/views.py

from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import random
from django.contrib.auth.decorators import login_required
from .models import GameResult

def index_view(request):
    return render(request, 'scholar/index.html')

@login_required
def add_view(request):
    return render(request, 'scholar/add.html')

@require_http_methods(["POST"])
def check_answer(request):
    data = json.loads(request.body)
    user_answer = data.get('userAnswer')
    correct_answer = data.get('correctAnswer')
    difficulty = data.get('difficulty')

    # Initialize the response dictionary
    response_data = {
        'is_correct': False,
        'next_question': {},
        'difficulty': difficulty
    }

    # Check if the user's answer is correct
    if user_answer == correct_answer:
        response_data['is_correct'] = True
        # Increase difficulty slightly
        difficulty = min(difficulty + 1, 10)  # Assuming a max difficulty level of 10
    else:
        # Decrease difficulty slightly, but not below 1
        difficulty = max(difficulty - 1, 1)

    # Generate the next question based on the new difficulty level
    num1 = random.randint(1, difficulty)
    num2 = random.randint(1, difficulty)
    response_data['next_question']['num1'] = num1
    response_data['next_question']['num2'] = num2
    response_data['next_question']['correctAnswer'] = num1 + num2
    response_data['difficulty'] = difficulty

    return JsonResponse(response_data)


@login_required
def multiply_view(request):
    return render(request, 'scholar/multiply.html')


@login_required
def save_game_result(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        GameResult.objects.create(
            task_type=data['task_type'],
            correct_answers_count=data['correct_answers_count'],
            wrong_answers_count=data['wrong_answers_count'],
            user=request.user
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)