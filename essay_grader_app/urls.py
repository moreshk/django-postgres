from django.urls import path
from . import views

app_name = 'essay_grader_app'  # Add this line

urlpatterns = [
    path('', views.index, name='index'),
]
