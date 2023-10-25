from django.urls import path
from . import views

app_name = 'v3essay_grader'

urlpatterns = [
    # your other url patterns here
    path('create_rubric/', views.create_rubric, name='create_rubric'),
    path('view_edit_rubric_criteria/', views.view_edit_rubric_criteria, name='view_edit_rubric_criteria'),
]