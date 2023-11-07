import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from v3essay_grader.models import Rubric, Criteria
from django.contrib import messages
from django.http import JsonResponse
from .v3grader import check_criteria
from .v3_5grader import check_criteria_combined_prompt
from users.models import GradeResult
import json
from .models import CombinedPromptResults
from django.http import JsonResponse
from django.core import serializers
from .models import SampleTopic
from django.views import View

@login_required
def create_rubric(request):
    if request.user.user_type == 'STUDENT':
        return redirect('home')
    
    if request.method == 'POST':
        # Create a new Rubric record
        Rubric.objects.create(
            creater_id=request.user.id,
            name=request.POST['nameInput'],
            state=request.POST['stateInput'],
            city=request.POST['cityInput'],
            school=request.POST['schoolInput'],
            essay_type=request.POST['essayTypeInput'],
            grade=request.POST['gradeInput'],
            curriculum=request.POST['curriculumInput']
        )
        messages.success(request, 'Rubric created. You can now add/edit criteria to it by going to View/Edit Rubric criteria.')
        return redirect('v3essay_grader:create_rubric')  # or wherever you want to redirect after form submission

    return render(request, 'v3essay_grader/create_rubric.html')

@login_required
def view_edit_rubric_criteria(request):
    if request.user.user_type == 'STUDENT':
        return redirect('home')
    
    user_rubrics = Rubric.objects.filter(creater_id=request.user.id).prefetch_related('criteria_set')
    other_rubrics = Rubric.objects.filter(creater_id=21).prefetch_related('criteria_set')  # Rubrics created by user 21
    return render(request, 'v3essay_grader/view_edit_rubric_criteria.html', {'user_rubrics': user_rubrics, 'other_rubrics': other_rubrics})


@login_required
def add_criteria(request):
    if request.method == 'POST':
        rubric_id = request.POST.get('rubric_id')
        criteria_name = request.POST.get('criteria_name')
        max_score = request.POST.get('max_score')
        criteria_desc = request.POST.get('description')
        spell_check = request.POST.get('spell_check') == 'true'

        rubric = Rubric.objects.get(id=rubric_id)

        criteria = Criteria.objects.create(
            rubric=rubric,
            criteria_name=criteria_name,
            max_score=max_score,
            criteria_desc=criteria_desc,
            spell_check=spell_check
        )

        return JsonResponse({'status': 'success'})
    

@login_required
def edit_criteria(request):
    if request.method == 'POST':
        criteria_id = request.POST.get('criteria_id')
        criteria_name = request.POST.get('criteria_name')
        max_score = request.POST.get('max_score')
        criteria_desc = request.POST.get('description')
        spell_check = request.POST.get('spell_check') == 'true'
        criteria = Criteria.objects.get(id=criteria_id)
        criteria.criteria_name = criteria_name
        criteria.max_score = max_score
        criteria.criteria_desc = criteria_desc
        criteria.spell_check = spell_check
        criteria.save()

        return JsonResponse({'status': 'success'})
    
@login_required
def delete_criteria(request):
    if request.method == 'POST':
        criteria_id = request.POST.get('criteria_id')

        criteria = Criteria.objects.get(id=criteria_id)
        criteria.delete()

        return JsonResponse({'status': 'success'})
    

@login_required
def custom_rubric_essay_grader(request):
    return render(request, 'v3essay_grader/custom_rubric_essay_grader.html')



# 1
@login_required
def grade_essay_criteria(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_response = data.get('user_response')
        title = data.get('title')
        description = data.get('description')
        essay_type = data.get('essay_type')
        grade = data.get('grade')
        rubric_id = data.get('rubric_id')  # Add this line
        assignment_name = data.get('assignment_name')
        student_name = data.get('student_name')
        
        print("I am in grade essay criteria")
        print(user_response, title, description, essay_type, grade, rubric_id, assignment_name, student_name)
        feedback_from_api = check_criteria(request, user_response, title, description, essay_type, grade, rubric_id, assignment_name, student_name)

        if feedback_from_api in ["No criteria in the rubric.", "Rubric with the provided ID does not exist."]:
                    print("error",feedback_from_api)
                    return JsonResponse({'error': feedback_from_api})

        return JsonResponse({'feedback': feedback_from_api})

    return JsonResponse({'error': 'Invalid method or missing parameters'}, status=400)


@login_required
def get_rubrics(request):
    user = request.user
    rubrics = Rubric.objects.filter(creater_id__in=[user.id, 21])  # Fetch rubrics created by the logged-in user or user with id 21 : Rubrics created by Sean
    rubrics_list = list(rubrics.values('id', 'name'))  # Convert the QuerySet to a list of dictionaries
    return JsonResponse(rubrics_list, safe=False)  # Return the list as a JSON response

@login_required
def view_grades(request):
    try:
        user_id = request.user.id
        assignment_name = request.GET.get('assignment_name', None)
        student_name = request.GET.get('student_name', None)

        user_grades = GradeResult.objects.filter(user_id=user_id)

        assignment_names = user_grades.values_list('assignment_name', flat=True).distinct()

        if assignment_name:
            user_grades = user_grades.filter(assignment_name=assignment_name)

        # Move this line here
        student_names = user_grades.values_list('student_name', flat=True).distinct()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(list(student_names), safe=False)

        context = {
            'grades': user_grades,
            'assignment_names': assignment_names,
            'student_names': student_names,
            'selected_assignment_name': assignment_name,
            'selected_student_name': student_name,
        }

        return render(request, 'v3essay_grader/view_grades.html', context)
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': str(e)}, status=500)
        raise  

@login_required
def filter_grades(request):
    user_id = request.user.id
    assignment_name = request.GET.get('assignment_name', '')
    student_name = request.GET.get('student_name', '')

    grades = GradeResult.objects.filter(user_id=user_id, assignment_name=assignment_name, student_name=student_name).values()

    # Ensure the response is always a list
    grades_list = list(grades)

    return JsonResponse(grades_list, safe=False)

@login_required
def pipeline(request):
    return render(request, 'v3essay_grader/pipeline.html')

@login_required
def combined_prompt(request):
    return render(request, 'v3essay_grader/combined_prompt.html')


# 1
@login_required
def grade_essay_combined_prompt(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_response = data.get('user_response')
        title = data.get('title')
        description = data.get('description')
        essay_type = data.get('essay_type')
        grade = data.get('grade')
        rubric_id = data.get('rubric_id')  # Add this line
        assignment_name = data.get('assignment_name')
        student_name = data.get('student_name')
        
        print("I am in grade essay combined prompt view")
        print(user_response, title, description, essay_type, grade, rubric_id, assignment_name, student_name)
        feedback_from_api = check_criteria_combined_prompt(request, user_response, title, description, essay_type, grade, rubric_id, assignment_name, student_name)

        if feedback_from_api in ["No criteria in the rubric.", "Rubric with the provided ID does not exist."]:
                    print("error",feedback_from_api)
                    return JsonResponse({'error': feedback_from_api})

        return JsonResponse({'feedback': feedback_from_api})

    return JsonResponse({'error': 'Invalid method or missing parameters'}, status=400)

@login_required
def view_combined_grades(request):
    user_id = request.user.id
    results = CombinedPromptResults.objects.filter(user_id=user_id)

    # Apply filters if they are provided
    essay_type = request.GET.get('essay_type')
    if essay_type and essay_type != '':
        results = results.filter(essay_type=essay_type)

    grade = request.GET.get('grade')
    if grade and grade != '':
        results = results.filter(grade=grade)

    rubric_name = request.GET.get('rubric_name')
    if rubric_name and rubric_name != '':
        results = results.filter(rubric_name=rubric_name)

    assignment_name = request.GET.get('assignment_name')
    if assignment_name and assignment_name != '':
        results = results.filter(assignment_name=assignment_name)

    student_name = request.GET.get('student_name')
    if student_name and student_name != '':
        results = results.filter(student_name=student_name)

    # If the request is AJAX, return the filtered results as JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = serializers.serialize('json', results)
        return JsonResponse(data, safe=False)

    # Otherwise, render the template
    context = {
        'results': results,
        'essay_types': results.values_list('essay_type', flat=True).distinct(),
        'grades': results.values_list('grade', flat=True).distinct(),
        'rubric_names': results.values_list('rubric_name', flat=True).distinct(),
        'assignment_names': results.values_list('assignment_name', flat=True).distinct(),
        'student_names': results.values_list('student_name', flat=True).distinct(),
    }
    return render(request, 'v3essay_grader/view_combined_grades.html', context)


@login_required
def dynamic_prompt(request):
    essay_types = SampleTopic.objects.values_list('essay_type', flat=True).distinct()
    grades = SampleTopic.objects.values_list('grade', flat=True).distinct().order_by('grade')
    return render(request, 'v3essay_grader/dynamic_prompt.html', {'essay_types': essay_types, 'grades': grades})

@login_required
def get_titles_and_descriptions(request):
    print("I am in get titles and descriptions")
    essay_type = request.GET.get('essay_type', None)
    if essay_type:
        essay_type = essay_type.lower()
    grade = request.GET.get('grade', None)

    if essay_type and grade:
        data = SampleTopic.objects.filter(essay_type=essay_type, grade=grade).values('essay_title', 'essay_description')
        print(data)
        return JsonResponse(list(data), safe=False)

    return JsonResponse({"error": "Invalid parameters"}, status=400)