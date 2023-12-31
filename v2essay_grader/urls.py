from django.urls import path
from . import views

app_name = 'v2essay_grader'  # Add this line

urlpatterns = [
    # Example path: path('example/', views.example_view, name='example_view_name'),
    path('', views.index, name='index'),
    path('grade_essay/', views.grade_essay, name='grade_essay'),
    path('hello_world/', views.hello_world_view, name='hello_world'),
    path('grade_essay_audience/', views.grade_essay_audience, name='grade_essay_audience'),
    path('grade_essay_text_structure/', views.grade_essay_text_structure, name='grade_essay_text_structure'),
    path('grade_essay_ideas/', views.grade_essay_ideas, name='grade_essay_ideas'),
    path('grade_essay_persuasive_devices/', views.grade_essay_persuasive_devices, name='grade_essay_persuasive_devices'),
    path('grade_essay_vocabulary/', views.grade_essay_vocabulary, name='grade_essay_vocabulary'),
    path('grade_essay_cohesion/', views.grade_essay_cohesion, name='grade_essay_cohesion'),
    path('grade_essay_paragraphing/', views.grade_essay_paragraphing, name='grade_essay_paragraphing'),
    path('grade_essay_sentence_structure/', views.grade_essay_sentence_structure, name='grade_essay_sentence_structure'),
    path('grade_essay_punctuation/', views.grade_essay_punctuation, name='grade_essay_punctuation'),
    path('grade_essay_spelling/', views.grade_essay_spelling, name='grade_essay_spelling'),
    path('grade_narrative_audience/', views.grade_narrative_audience, name='grade_narrative_audience'),
    path('grade_narrative_text_structure/', views.grade_narrative_text_structure, name='grade_narrative_text_structure'),
    path('grade_narrative_ideas/', views.grade_narrative_ideas, name='grade_narrative_ideas'),
    path('grade_narrative_setting/', views.grade_narrative_setting, name='grade_narrative_setting'),
    path('grade_narrative_cohesion/', views.grade_narrative_cohesion, name='grade_narrative_cohesion'),
    path('essay_input/', views.essay_input, name='essay_input'),
    path('create_assignment/', views.create_assignment, name='create_assignment'),
]

