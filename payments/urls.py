from django.urls import path
from . import views


app_name = 'payments'

urlpatterns = [
    path('billing/', views.billing, name='billing'),
    path('billing/<int:plan_id>/', views.billing, name='billing_with_plan'),
    path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('select-subscription/', views.select_subscription, name='select_subscription'),
    path('success/', views.success_page, name='success_page'),
    # Other payment-related URL patterns
]
