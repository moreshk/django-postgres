import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from v3essay_grader.models import Rubric, Criteria
from django.contrib import messages
from django.http import JsonResponse
from .v3grader import check_spelling_persuasive, check_criteria
from users.models import GradeResult
import json

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
    
    rubrics = Rubric.objects.filter(creater_id=request.user.id).prefetch_related('criteria_set')
    return render(request, 'v3essay_grader/view_edit_rubric_criteria.html', {'rubrics': rubrics})

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
    rubrics = Rubric.objects.filter(creater_id__in=[user.id, 2])  # Fetch rubrics created by the logged-in user or user with id 2
    rubrics_list = list(rubrics.values('id', 'name'))  # Convert the QuerySet to a list of dictionaries
    return JsonResponse(rubrics_list, safe=False)  # Return the list as a JSON response



@login_required
def view_grades(request):
    user_id = request.user.id
    user_grades = GradeResult.objects.filter(user_id=user_id)

    assignment_names = user_grades.values_list('assignment_name', flat=True).distinct()
    student_names = user_grades.values_list('student_name', flat=True).distinct()

    context = {
        'grades': user_grades,
        'assignment_names': assignment_names,
        'student_names': student_names,
    }

    return render(request, 'v3essay_grader/view_grades.html', context)

@login_required
def filter_grades(request):
    user_id = request.user.id
    assignment_name = request.GET.get('assignment_name', '')
    student_name = request.GET.get('student_name', '')

    grades = GradeResult.objects.filter(user_id=user_id, assignment_name=assignment_name, student_name=student_name).values()

    return JsonResponse(list(grades), safe=False)