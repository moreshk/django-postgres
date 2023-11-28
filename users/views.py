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
from .models import Assignment

from django.contrib.auth import get_user_model
from .forms import UserUpdateForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.conf import settings
from django.template.loader import render_to_string

from django import forms
from django.contrib.auth import get_user_model

from .forms import SchoolForm
from .models import School
from payments.models import UserSubscription

from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

from .models import CustomUser
from .models import GlobalSettings

User = get_user_model()

# Initialize a logger
logger = logging.getLogger(__name__)


def register(request):
    if 'referrer_id' not in request.session:
        # Redirect the user to a page that tells them to use a referral link
        return redirect('referral_required')

    context = {}
    if 'referral_error' in request.session:
        context['referral_error'] = request.session['referral_error']
        del request.session['referral_error']

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to the database yet
            user.is_active = False  # Set user as inactive until they verify their email
            
            if 'special_onboarding' in request.session:
                user.user_type = 'LABELLER'
                del request.session['special_onboarding']

            # If there's a referrer_id in the session, set the referred_by field
            if 'referrer_id' in request.session:
                user.referred_by_id = request.session['referrer_id']
                del request.session['referrer_id']

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

    protocol = 'https' if request.is_secure() else 'http'
    activate_url = f'{protocol}://{domain}{link}'


    # activate_url = 'http://' + domain + link
    
    email_subject = 'Activate your account'
    
    # Render the email template with the activation link
    email_body = render_to_string('users/verification_email.html', {'activate_url': activate_url})
    
    email = EmailMessage(email_subject, email_body, settings.VERIFIED_SENDER_EMAIL, [user.email])
    email.content_subtype = 'html'  # This is essential. It tells that the email has HTML content.
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
                if user.has_completed_onboarding:
                    return redirect('home')
                else:
                    return redirect('onboarding_first_name')
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
        # logger.error(f"Error during activation: {ex}")
        logger.error("Error during activation", exc_info=True)
        pass
    return render(request, 'users/activation_failed.html')

def email_verification_sent(request):
    return render(request, 'users/email_verification_sent.html')


@login_required
def myaccount(request):
    user_subscription = UserSubscription.objects.filter(user=request.user, is_active=True).first()
    user_form = UserUpdateForm(instance=request.user, data=request.POST or None)
    password_form = CustomPasswordChangeForm(request.user, data=request.POST or None)

    # Fetch the bonus from the GlobalSettings
    global_settings = GlobalSettings.objects.first()
    referred_user_bonus = global_settings.referred_user_bonus

    if request.method == 'POST':
        details_updated = False

        # Check if user details form is valid and save
        if user_form.is_valid():
            user_form.save()
            details_updated = True

        if request.POST.get('old_password') and request.POST.get('new_password1'):
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, request.user)
                details_updated = True

        # Display a success message if any details were updated
        if details_updated:
            messages.success(request, 'Details updated!')

    referral_link = request.build_absolute_uri(reverse('register_with_referral', args=[request.user.referral_code]))

    return render(request, 'users/myaccount.html', {
        'user_form': user_form,
        'password_form': password_form,
        'user_subscription': user_subscription,
        'referral_link': referral_link,
        'referral_slots': request.user.referral_slots,
        'referred_user_bonus': referred_user_bonus,  # Pass the bonus to the template
    })

@login_required
def home(request):
    user_type = request.user.user_type  # Get the user type
    return render(request, 'users/home.html', {'user_type': user_type})

@login_required
def onboarding_first_name(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        if first_name:
            request.user.first_name = first_name
            request.user.save()
            return redirect('onboarding_last_name')
    return render(request, 'users/onboarding_first_name.html')

@login_required
def onboarding_last_name(request):
    if request.method == 'POST':
        last_name = request.POST.get('last_name')
        if last_name:
            request.user.last_name = last_name
            request.user.save()
        
            if request.user.user_type == 'LABELLER':
                return redirect('onboarding_wallet')
            else:
                return redirect('onboarding_user_type')
    
    return render(request, 'users/onboarding_last_name.html')

User = get_user_model()

class UserTypeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_type']
        widgets = {
            'user_type': forms.RadioSelect
        }

@login_required
def onboarding_user_type(request):
    form = UserTypeForm()  # Replace with your actual form
    if request.method == 'POST':
        form = UserTypeForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data.get('user_type')
            request.user.user_type = user_type
            request.user.has_completed_onboarding = True
            request.user.save()
            return redirect('home')
    return render(request, 'users/onboarding_user_type.html', {'form': form})

@login_required
def view_assignments(request):
    # Fetch assignments that match the teacher_id of the logged in user
    assignments = Assignment.objects.filter(teacher_id=request.user.id)
    return render(request, 'users/view_assignments.html', {'assignments': assignments})



def create_school(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            school = form.save(commit=False)
            school.admin_id = request.user.id
            school.status = 'live'
            school.save()
            messages.success(request, 'School successfully created.')
            return redirect('create_school')
    else:
        form = SchoolForm()
    return render(request, 'users/create_school.html', {'form': form})



@receiver(post_save, sender=CustomUser)
def create_referral_code(sender, instance, created, **kwargs):
    if created and not instance.referral_code:
        instance.referral_code = str(uuid.uuid4())[:8]
        instance.save()


def register_with_referral(request, code):
    try:
        referrer = CustomUser.objects.get(referral_code=code)
        if referrer.referral_slots <= 0:
            # Redirect the user to a page that tells them the referral code has been exhausted
            return redirect('referral_exhausted')
        request.session['referrer_id'] = referrer.id
        request.session.save()  # Manually save the session

        # Check if the referrer is a 'LABELLER'
        if referrer.user_type == 'LABELLER':
            request.session['special_onboarding'] = True
        elif code == '2bf453ad':
            request.session['special_onboarding'] = True

        return redirect('register')
    except CustomUser.DoesNotExist:
        # Redirect the user to a page that tells them to use a valid referral link
        return redirect('referral_required')


@login_required
def onboarding_wallet(request):
    if request.method == 'POST':
        wallet = request.POST.get('wallet')
        language = request.POST.get('language')
        if wallet:
            request.user.wallet = wallet
            request.user.language = language
            request.user.has_completed_onboarding = True  # Set the onboarding complete flag to True

            # Fetch the bonuses from the GlobalSettings
            global_settings = GlobalSettings.objects.first()
            referring_user_bonus = global_settings.referring_user_bonus
            referred_user_bonus = global_settings.referred_user_bonus

            # Increase the token balance of the new user and the referring user by the respective bonuses
            if request.user.referred_by:
                request.user.token += referred_user_bonus
                request.user.referred_by.token += referring_user_bonus
                request.user.referred_by.save()

            request.user.save()
            return redirect('home')
    return render(request, 'users/onboarding_wallet.html')


@receiver(post_save, sender=CustomUser)
def update_referral_slots(sender, instance, created, **kwargs):
    print("I am triggering update referral slots")
    print("Created", created)
    print("Referred by ", instance.referred_by)
    if created and instance.referred_by:
        print("I am in the reduce referral slots conditional code")
        referrer = instance.referred_by
        print("Referred by", referrer)
        print("Referral slots ", referrer.referral_slots)
        referrer.referral_slots -= 1
        print("I have reduced referral slots, new referral slots are ", referrer.referral_slots)
        referrer.save()


def referral_required(request):
    return render(request, 'users/referral_required.html')

def referral_exhausted(request):
    return render(request, 'users/referral_exhausted.html')