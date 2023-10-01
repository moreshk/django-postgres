# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .generator import generate_test  # Import the function


@login_required
def index(request):
    message = ""
    if request.method == "POST" and "generate_test" in request.POST:
        message = generate_test()
    return render(request, 'essay_grader_app/index.html', {'message': message})
