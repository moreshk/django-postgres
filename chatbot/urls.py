from django.urls import path
from .views import personal_tutor_view, personal_tutor_interface, topics_view, text_to_speech_view

app_name = 'chatbot'  # Define the app namespace

urlpatterns = [
    path('personal-tutor/', personal_tutor_interface, name='personal_tutor_interface'),
    path('personal-tutor/chat/', personal_tutor_view, name='personal_tutor_view'),
    path('topics/', topics_view, name='topics'),
    path('text-to-speech/', text_to_speech_view, name='text_to_speech'),  # Add this line
]