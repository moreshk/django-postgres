# scholar/urls.py

from django.urls import path
from .views import index_view, add_view, check_answer, multiply_view

app_name = 'scholar'  # Define the app namespace

urlpatterns = [
    path('', index_view, name='index'),
    path('add/', add_view, name='add'),
    path('check_answer/', check_answer, name='check_answer'),
    path('multiply/', multiply_view, name='multiply'),
]