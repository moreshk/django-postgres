# translator/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('random_sentence/<str:topic>/', views.random_sentence, name='random_sentence'),
    path('user_translations/', views.user_translations, name='user_translations'),
    path('babbl/', views.topics, name='topics'),
]