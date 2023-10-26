from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from v3essay_grader.models import Rubric
from django.contrib import messages

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