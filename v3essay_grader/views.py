from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from v3essay_grader.models import Rubric, Criteria
from django.contrib import messages
from django.http import JsonResponse

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
    
    # rubrics = Rubric.objects.filter(creater_id=request.user.id)
    # return render(request, 'v3essay_grader/view_edit_rubric_criteria.html', {'rubrics': rubrics})

    rubrics = Rubric.objects.filter(creater_id=request.user.id).prefetch_related('criteria_set')
    return render(request, 'v3essay_grader/view_edit_rubric_criteria.html', {'rubrics': rubrics})

@login_required
def add_criteria(request):
    if request.method == 'POST':
        rubric_id = request.POST.get('rubric_id')
        criteria_name = request.POST.get('criteria_name')
        max_score = request.POST.get('max_score')
        criteria_desc = request.POST.get('description')

        rubric = Rubric.objects.get(id=rubric_id)

        criteria = Criteria.objects.create(
            rubric=rubric,
            criteria_name=criteria_name,
            max_score=max_score,
            criteria_desc=criteria_desc
        )

        return JsonResponse({'status': 'success'})
    

@login_required
def edit_criteria(request):
    if request.method == 'POST':
        criteria_id = request.POST.get('criteria_id')
        criteria_name = request.POST.get('criteria_name')
        max_score = request.POST.get('max_score')
        criteria_desc = request.POST.get('description')

        criteria = Criteria.objects.get(id=criteria_id)
        criteria.criteria_name = criteria_name
        criteria.max_score = max_score
        criteria.criteria_desc = criteria_desc
        criteria.save()

        return JsonResponse({'status': 'success'})
    
@login_required
def delete_criteria(request):
    if request.method == 'POST':
        criteria_id = request.POST.get('criteria_id')

        criteria = Criteria.objects.get(id=criteria_id)
        criteria.delete()

        return JsonResponse({'status': 'success'})