# scholar/urls.py

from django.urls import path
from .views import index_view, add_view, check_answer, multiply_view, save_game_result, my_scores_view, leaderboard_view, subtract_view, youtube_viewer, record_youtube_time, check_screen_time

app_name = 'scholar'  # Define the app namespace

urlpatterns = [
    path('', index_view, name='index'),
    path('add/', add_view, name='add'),
    path('check_answer/', check_answer, name='check_answer'),
    path('multiply/', multiply_view, name='multiply'),
    path('save_game_result/', save_game_result, name='save_game_result'),
    path('my_scores/', my_scores_view, name='my_scores'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
    path('subtract/', subtract_view, name='subtract'),
    path('youtube_viewer/', youtube_viewer, name='youtube_viewer'),
    path('record_youtube_time/', record_youtube_time, name='record_youtube_time'),
    path('check_screen_time/', check_screen_time, name='check_screen_time'),
]