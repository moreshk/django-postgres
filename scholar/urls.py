# scholar/urls.py

from django.urls import path
from .views import index_view, add_view, check_answer, multiply_view, save_game_result, my_scores_view, leaderboard_view

app_name = 'scholar'  # Define the app namespace

urlpatterns = [
    path('', index_view, name='index'),
    path('add/', add_view, name='add'),
    path('check_answer/', check_answer, name='check_answer'),
    path('multiply/', multiply_view, name='multiply'),
    path('save_game_result/', save_game_result, name='save_game_result'),
    path('my_scores/', my_scores_view, name='my_scores'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
]