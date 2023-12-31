from django.urls import path
from .views import chatbot_view, chat_interface

app_name = 'chatbot'  # Define the app namespace

urlpatterns = [
    path('chat/', chatbot_view, name='chatbot_view'),
    path('chat-interface/', chat_interface, name='chat_interface'),  # Add this line
]