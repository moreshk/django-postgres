from django.urls import path
from . import views
from .views import claim_bonus, label_task_view

urlpatterns = [
    path('candlestick/', views.candlestick_view, name='candlestick_view'),
    path('back/', views.back_view, name='back_view'),
    path('forward/', views.forward_view, name='forward_view'),
    path('check_doji/', views.check_doji, name='check_doji'),
    path('referred_users/', views.referred_users_view, name='referred_users_view'),
    path('training/<int:course_id>/', views.training, name='training'),
    path('courses/', views.courses_view, name='courses'),
    path('previous_lesson/<int:course_id>/', views.previous_lesson, name='previous_lesson'),
    path('next_lesson/<int:course_id>/', views.next_lesson, name='next_lesson'),
    path('claim_bonus/<int:course_id>/', claim_bonus, name='claim_bonus'),
    path('label_task/', label_task_view, name='label_task_view'),
]