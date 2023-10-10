from django.urls import path
from . import views


app_name = 'payments'

urlpatterns = [
    path('billing/', views.billing, name='billing'),
    path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),
    # Other payment-related URL patterns
]
