from django.urls import path
from . import views

app_name = 'v3essay_grader'

urlpatterns = [
    # your other url patterns here
    path('create_rubric/', views.create_rubric, name='create_rubric'),
    path('view_edit_rubric_criteria/', views.view_edit_rubric_criteria, name='view_edit_rubric_criteria'),
    path('add_criteria/', views.add_criteria, name='add_criteria'),
    path('edit_criteria/', views.edit_criteria, name='edit_criteria'),
    path('delete_criteria/', views.delete_criteria, name='delete_criteria'),
    path('custom_rubric_essay_grader/', views.custom_rubric_essay_grader, name='custom_rubric_essay_grader'),
    path('get_rubrics/', views.get_rubrics, name='get_rubrics'),
    path('grade_essay_criteria/', views.grade_essay_criteria, name='grade_essay_criteria'),
    path('view-grades/', views.view_grades, name='view-grades'),
    path('filter_grades/', views.filter_grades, name='filter-grades'),
]