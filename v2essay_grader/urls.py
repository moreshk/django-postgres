from django.urls import path
from . import views

urlpatterns = [
    # Example path: path('example/', views.example_view, name='example_view_name'),
    path('', views.index, name='index'),
]
