from django.urls import path
from .views import chatbot_view, chat_interface, personal_tutor_view, personal_tutor_interface, topics_view

app_name = 'chatbot'  # Define the app namespace

urlpatterns = [
    path('chat/', chatbot_view, name='chatbot_view'),
    path('chat-interface/', chat_interface, name='chat_interface'),
    path('personal-tutor/', personal_tutor_interface, name='personal_tutor_interface'),
    path('personal-tutor/chat/', personal_tutor_view, name='personal_tutor_view'),
    path('topics/', topics_view, name='topics'),
]