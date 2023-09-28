from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.urls import reverse

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.contrib.auth import get_user_model
from .forms import UserUpdateForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash

User = get_user_model()

# Initialize a logger
logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to the database yet
            user.is_active = False  # Set user as inactive until they verify their email
            user.save()  # Now save to the database

            # Send the verification email
            send_verification_email(request, user)

            # Redirect to a page that tells the user to check their email
            return redirect('email_verification_sent')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})




def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
    activate_url = 'http://' + domain + link
    email_subject = 'Activate your account'
    email_body = 'Hi, please use this link to verify your account: ' + activate_url
    email = EmailMessage(email_subject, email_body, 'noreply@mydomain.com', [user.email])
    email.send()

def user_login(request):
    context = {}
    if request.method == 'POST':
        
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('myaccount')
            else:
                context['error'] = "Your account is not active. Please verify your email."
        else:
            context['error'] = "Invalid username or password."
    return render(request, 'users/login.html', context)

def user_logout(request):
    logout(request)
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated successfully. Please login to continue.')
            return redirect('login')  # Redirect to the login page
        else:
            return render(request, 'users/activation_failed.html')
    except Exception as ex:
        logger.error(f"Error during activation: {ex}")
        pass
    return render(request, 'users/activation_failed.html')

def email_verification_sent(request):
    return render(request, 'users/email_verification_sent.html')

# @login_required
# def myaccount(request):
#     if request.method == 'POST':
#         user_form = UserUpdateForm(request.POST, instance=request.user)
#         password_form = CustomPasswordChangeForm(request.user, request.POST)

#         if user_form.is_valid():
#             user_form.save()
#             messages.success(request, 'Details updated!')

#         # Check if either the old password field or new password field is filled out
#         if request.POST.get('old_password') or request.POST.get('new_password1'):
#             if password_form.is_valid():
#                 password_form.save()
#                 # Update the session with the new password hash to keep the user logged in
#                 update_session_auth_hash(request, request.user)
#                 messages.success(request, 'Password updated!')
#             else:
#                 # Add the form errors to the messages to display them to the user
#                 for field, errors in password_form.errors.items():
#                     for error in errors:
#                         messages.error(request, f"{field}: {error}")

#         return redirect('myaccount')
#     else:
#         user_form = UserUpdateForm(instance=request.user)
#         password_form = CustomPasswordChangeForm(request.user)

#     return render(request, 'users/myaccount.html', {
#         'user_form': user_form,
#         'password_form': password_form
#     })

@login_required
def myaccount(request):
    user_form = UserUpdateForm(instance=request.user, data=request.POST or None)
    password_form = CustomPasswordChangeForm(request.user, data=request.POST or None)

    if request.method == 'POST':
        details_updated = False

        # Check if user details form is valid and save
        if user_form.is_valid():
            user_form.save()
            details_updated = True

        # Check if password form fields are filled and form is valid
        if (request.POST.get('old_password') or request.POST.get('new_password1')) and password_form.is_valid():
            password_form.save()
            # Update the session to keep the user logged in after password change
            update_session_auth_hash(request, request.user)
            details_updated = True

        # Display a success message if any details were updated
        if details_updated:
            messages.success(request, 'Details updated!')

    return render(request, 'users/myaccount.html', {
        'user_form': user_form,
        'password_form': password_form
    })