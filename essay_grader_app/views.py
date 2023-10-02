# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .generator import generate_test_data, grade_essay

@login_required
def index(request):
    message = ""
    feedback = ""
    if request.method == "POST":
        if "generate_test" in request.POST:
            message = generate_test_data()
            # Assuming the message format is "Title: xxx\nDescription: yyy"
            title, description = message.split("\n")
            request.session['task_title'] = title.split(":")[1].strip()
            request.session['task_description'] = description.split(":")[1].strip()
        elif "text_input" in request.POST:
            user_response = request.POST.get('text_input')
            title = request.session.get('task_title', 'Default Title')  # You can fetch this from the session or database
            description = request.session.get('task_description', 'Default Description')  # You can fetch this from the session or database
            feedback = grade_essay(user_response, title, description)
    return render(request, 'essay_grader_app/index.html', {'message': message, 'feedback': feedback})
