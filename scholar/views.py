# scholar/views.py

from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import random
from django.contrib.auth.decorators import login_required
from .models import GameResult, ScreenTime
from django.template import loader
from django.db.models import Sum
import os

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
    operation = data.get('operation', 'addition')  # Default to 'addition' if not specified

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
    num1 = random.randint(1, difficulty * 10)  # Adjust the range as needed
    num2 = random.randint(1, difficulty * 10)

    # Ensure num1 is greater than num2 for subtraction
    if operation == 'subtraction':
        num1, num2 = max(num1, num2), min(num1, num2)
        response_data['next_question']['correctAnswer'] = num1 - num2
    else:
        response_data['next_question']['correctAnswer'] = num1 + num2

    response_data['next_question']['num1'] = num1
    response_data['next_question']['num2'] = num2
    response_data['difficulty'] = difficulty

    return JsonResponse(response_data)


@login_required
def multiply_view(request):
    return render(request, 'scholar/multiply.html')


@login_required
def save_game_result(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        correct_answers_count = data['correct_answers_count']
        
        # Save GameResult
        GameResult.objects.create(
            task_type=data['task_type'],
            correct_answers_count=correct_answers_count,
            wrong_answers_count=data['wrong_answers_count'],
            user=request.user
        )
        
        # Save ScreenTime
        ScreenTime.objects.create(
            user=request.user,
            operation=data['task_type'],
            minutes=correct_answers_count  # Assuming 1 minute per correct answer
        )
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def my_scores_view(request):
    # Fetch the latest 20 scores for each category for the current user
    addition_scores = GameResult.objects.filter(
        user=request.user, task_type='addition'
    ).order_by('-timestamp')[:20]

    multiplication_scores = GameResult.objects.filter(
        user=request.user, task_type='multiplication'
    ).order_by('-timestamp')[:20]

    subtraction_scores = GameResult.objects.filter(
        user=request.user, task_type='subtraction'
    ).order_by('-timestamp')[:20]

    # Calculate the total correct answers for each category
    addition_total = sum(score.correct_answers_count for score in addition_scores)
    multiplication_total = sum(score.correct_answers_count for score in multiplication_scores)
    subtraction_total = sum(score.correct_answers_count for score in subtraction_scores)

    # Calculate the available screen time
    available_screen_time = get_available_screen_time(request.user)

    context = {
        'addition_scores': addition_scores,
        'multiplication_scores': multiplication_scores,
        'subtraction_scores': subtraction_scores,
        'addition_total': addition_total,
        'multiplication_total': multiplication_total,
        'subtraction_total': subtraction_total,
        'available_screen_time': available_screen_time,  # Add this line
    }
    return render(request, 'scholar/my_scores.html', context)

def leaderboard_view(request):
    # Fetch the top 10 addition scores
    addition_leaderboard = GameResult.objects.filter(
        task_type='addition'
    ).order_by('-correct_answers_count')[:5]

    # Fetch the top 10 multiplication scores
    multiplication_leaderboard = GameResult.objects.filter(
        task_type='multiplication'
    ).order_by('-correct_answers_count')[:5]

    # Fetch the top 10 subtraction scores
    subtraction_leaderboard = GameResult.objects.filter(
        task_type='subtraction'
    ).order_by('-correct_answers_count')[:5]


    context = {
        'addition_leaderboard': addition_leaderboard,
        'multiplication_leaderboard': multiplication_leaderboard,
        'subtraction_leaderboard': subtraction_leaderboard,  # Add this line
    }
    return render(request, 'scholar/leaderboard.html', context)


@login_required
def subtract_view(request):
    return render(request, 'scholar/subtract.html')

@login_required
def youtube_viewer(request):
    context = {
        'YOUTUBE_API_KEY': os.environ.get('YOUTUBE_API_KEY')
    }
    return render(request, 'scholar/youtube_viewer.html', context)


# scholar/views.py

@login_required
@require_http_methods(["POST"])
def record_youtube_time(request):
    data = json.loads(request.body)
    video_id = data.get('videoId')
    minutes_watched = int(data.get('minutes', 0))
    
    # Check if the user has available screen time
    available_time = get_available_screen_time(request.user)
    if available_time <= 0:
        # User has no screen time left, do not record and inform the client
        return JsonResponse({'status': 'success', 'is_allowed': False})
    
    # User has screen time left, record the screen time
    ScreenTime.objects.create(
        user=request.user,
        operation='youtube',
        minutes=minutes_watched
    )
    
    return JsonResponse({'status': 'success', 'is_allowed': True})


def get_available_screen_time(user):
    earned_time = ScreenTime.objects.filter(
        user=user,
        operation__in=['addition', 'multiplication', 'subtraction']
    ).aggregate(total_minutes=Sum('minutes'))['total_minutes'] or 0
    
    used_time = ScreenTime.objects.filter(
        user=user,
        operation='youtube'
    ).aggregate(total_minutes=Sum('minutes'))['total_minutes'] or 0
    
    return earned_time - used_time

# scholar/views.py

@login_required
@require_http_methods(["POST"])
def check_screen_time(request):
    available_time = get_available_screen_time(request.user)
    return JsonResponse({
        'is_allowed': available_time > 0,
        'available_time': available_time
    })