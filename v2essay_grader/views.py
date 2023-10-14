import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import JsonResponse
from .v2grader import check_relevance, hello_world, check_audience_persuasive, check_text_structure_persuasive
from .v2grader import check_ideas_persuasive, check_persuasive_devices_persuasive

@login_required
def index(request):
    return render(request, 'v2essay_grader/index.html')

# 0
@login_required
def grade_essay(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_response = data.get('user_response')
        title = data.get('title')
        description = data.get('description')
        essay_type = data.get('essay_type')
        grade = data.get('grade')
        print("I am in grade essay check relevance")
        print(user_response, title, description, essay_type, grade)
        feedback_from_api = check_relevance(user_response, title, description, essay_type, grade)
        return JsonResponse({'feedback': feedback_from_api})

    return JsonResponse({'error': 'Invalid method or missing parameters'}, status=400)

@login_required
def hello_world_view(request):
    return JsonResponse({'message': hello_world()})

# 1
@login_required
def grade_essay_audience(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_response = data.get('user_response')
        title = data.get('title')
        description = data.get('description')
        essay_type = data.get('essay_type')
        grade = data.get('grade')
        print("I am in grade essay audience")
        print(user_response, title, description, essay_type, grade)
        feedback_from_api = check_audience_persuasive(user_response, title, description, essay_type, grade)
        return JsonResponse({'feedback': feedback_from_api})

    return JsonResponse({'error': 'Invalid method or missing parameters'}, status=400)

# 2
@login_required
def grade_essay_text_structure(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_response = data.get('user_response')
        title = data.get('title')
        description = data.get('description')
        essay_type = data.get('essay_type')
        grade = data.get('grade')
        print("I am in grade essay text structure")
        print(user_response, title, description, essay_type, grade)
        feedback_from_api = check_text_structure_persuasive(user_response, title, description, essay_type, grade)
        return JsonResponse({'feedback': feedback_from_api})

    return JsonResponse({'error': 'Invalid method or missing parameters'}, status=400)

# 3
@login_required
def grade_essay_ideas(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_response = data.get('user_response')
        title = data.get('title')
        description = data.get('description')
        essay_type = data.get('essay_type')
        grade = data.get('grade')
        print("I am in grade essay ideas")
        print(user_response, title, description, essay_type, grade)
        feedback_from_api = check_ideas_persuasive(user_response, title, description, essay_type, grade)
        return JsonResponse({'feedback': feedback_from_api})

    return JsonResponse({'error': 'Invalid method or missing parameters'}, status=400)

# 4
@login_required
def grade_essay_persuasive_devices(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_response = data.get('user_response')
        title = data.get('title')
        description = data.get('description')
        essay_type = data.get('essay_type')
        grade = data.get('grade')
        print("I am in grade essay audience")
        print(user_response, title, description, essay_type, grade)
        feedback_from_api = check_persuasive_devices_persuasive(user_response, title, description, essay_type, grade)
        return JsonResponse({'feedback': feedback_from_api})

    return JsonResponse({'error': 'Invalid method or missing parameters'}, status=400)