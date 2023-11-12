from django.urls import path
from . import views

urlpatterns = [
    path('candlestick/', views.candlestick_view, name='candlestick_view'),
    path('back/', views.back_view, name='back_view'),
    path('forward/', views.forward_view, name='forward_view'),
    path('check_doji/', views.check_doji, name='check_doji'),
]