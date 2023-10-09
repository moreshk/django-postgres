from django.urls import path
from . import views
from .views import incorrect_spelling


app_name = 'spellcheck'  # Add this line

urlpatterns = [
    path('', views.index, name='index'),
    path('incorrect_spelling/', incorrect_spelling, name='incorrect_spelling'),
]