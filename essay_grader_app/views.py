# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .generator import generate_test_data
from .grader import grade_essay  # Update this importfrom .grader import grade_essay  # Update this import

@login_required
# def index(request):
#     message = ""
#     feedback = ""
#     if request.method == "POST":
#         if "generate_test" in request.POST:
#             # Fetch the values from the dropdowns
#             exam_type = request.POST.get('examType')
#             essay_type = request.POST.get('essayType', '')  # This might be empty if the exam type is not NAPLAN
#             grade = request.POST.get('grade', '')  # This might be empty if the exam type is not NAPLAN

#             # Pass the values to the generate_test_data function
#             message = generate_test_data(exam_type, essay_type, grade)
#             # message = generate_test_data()   
#             # Assuming the message format is "Title: xxx\nDescription: yyy"
#             # title, description = message.split("\n")
#             segments = message.split("\n")
#             title = segments[0]
#             description = "\n".join(segments[1:])

#             request.session['task_title'] = title.split(":")[1].strip()
#             request.session['task_description'] = description.split(":")[1].strip()
#         elif "text_input" in request.POST:
#             user_response = request.POST.get('text_input')
#             title = request.session.get('task_title', 'Default Title')  # You can fetch this from the session or database
#             description = request.session.get('task_description', 'Default Description')  # You can fetch this from the session or database
#             feedback = grade_essay(user_response, title, description, exam_type, essay_type, grade)
#     return render(request, 'essay_grader_app/index.html', {'message': message, 'feedback': feedback})

def index(request):
    message = ""
    feedback = ""
    if request.method == "POST":
        if "generate_test" in request.POST:
            # Fetch the values from the dropdowns
            exam_type = request.POST.get('examType')
            essay_type = request.POST.get('essayType', '')  # This might be empty if the exam type is not NAPLAN
            grade = request.POST.get('grade', '')  # This might be empty if the exam type is not NAPLAN

            # Store the values in the session
            request.session['exam_type'] = exam_type
            request.session['essay_type'] = essay_type
            request.session['grade'] = grade

            # Pass the values to the generate_test_data function
            message = generate_test_data(exam_type, essay_type, grade)
            
            segments = message.split("\n")
            title = segments[0]
            description = "\n".join(segments[1:])

            request.session['task_title'] = title.split(":")[1].strip()
            request.session['task_description'] = description.split(":")[1].strip()
        elif "text_input" in request.POST:
            user_response = request.POST.get('text_input')
            title = request.session.get('task_title', 'Default Title')
            description = request.session.get('task_description', 'Default Description')
            
            # Fetch the values from the session
            exam_type = request.session.get('exam_type', 'Default Exam Type')
            essay_type = request.session.get('essay_type', 'Default Essay Type')
            grade = request.session.get('grade', 'Default Grade')

            feedback = grade_essay(user_response, title, description, exam_type, essay_type, grade)
    return render(request, 'essay_grader_app/index.html', {'message': message, 'feedback': feedback})
