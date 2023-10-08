from django.urls import path
from . import views

app_name = 'spellcheck'  # Add this line

urlpatterns = [
    path('', views.index, name='index'),
]