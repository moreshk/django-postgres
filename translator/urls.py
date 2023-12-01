# translator/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('random-sentence/', views.random_sentence, name='random_sentence'),
    path('user_translations/', views.user_translations, name='user_translations'),
]