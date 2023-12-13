"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views
from django.views.generic.base import RedirectView
from payments import views as payment_views
from django.conf import settings
from django.conf.urls.static import static
from users.views import register_with_referral



urlpatterns = [
    path("admin/", admin.site.urls),
    path('login/', views.user_login, name='login'),      # Assuming you have a user_login view
    path('logout/', views.user_logout, name='logout'),   # Assuming you have a user_logout view
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('', views.home, name='index'),
    path('email_verification_sent/', views.email_verification_sent, name='email_verification_sent'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('payments/', include('payments.urls')),
    path('essay_grader_app/', include('essay_grader_app.urls')),
    path('spellcheck/', include('spellcheck.urls')),
    path('home/', views.home, name='home'),
    path('v2essay_grader/', include('v2essay_grader.urls')),
    path('onboarding_first_name/', views.onboarding_first_name, name='onboarding_first_name'),
    path('onboarding_last_name/', views.onboarding_last_name, name='onboarding_last_name'),
    path('onboarding_user_type/', views.onboarding_user_type, name='onboarding_user_type'),
    path('view_assignments/', views.view_assignments, name='view_assignments'),
    path('create_school/', views.create_school, name='create_school'),
    path('v3essay_grader/', include('v3essay_grader.urls', namespace='v3essay_grader')),
    path('onboarding_wallet/', views.onboarding_wallet, name='onboarding_wallet'),
    path('labeller/', include('labeller.urls')),
    path('referral_required/', views.referral_required, name='referral_required'),
    path('referral_exhausted/', views.referral_exhausted, name='referral_exhausted'),
    path('register/<str:code>/', register_with_referral, name='register_with_referral'),
    path('register/', views.register, name='register'),  # Assuming you have a register view
    path('transcriber/', include('transcriber.urls')),
    path('translator/', include('translator.urls')),
    path('scholar/', include('scholar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


