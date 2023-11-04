import stripe
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import BillingForm
from .models import UserSubscription
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import SubscriptionPlan

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def select_subscription(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'payments/select_subscription.html', {'plans': plans})

@login_required
def billing(request, plan_id=None):
    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['stripe_token']
            plan = form.cleaned_data['subscription_plan']

            try:
                # Check if the user already has a Stripe Customer ID
                if not request.user.stripe_customer_id:
                    # Create a new Stripe Customer
                    customer = stripe.Customer.create(
                        email=request.user.email,
                        name=f'{request.user.first_name} {request.user.last_name}',
                    )
                    request.user.stripe_customer_id = customer.id
                    request.user.save()
                    customer_id = customer.id
                else:
                    # Use the existing Stripe Customer ID
                    customer_id = request.user.stripe_customer_id

                # Attach the card to the customer
                stripe.Customer.modify(
                    customer_id,
                    source=token,
                )

                # Create a new subscription using Stripe SDK
                subscription = stripe.Subscription.create(
                    customer=customer_id,
                    items=[{'plan': plan.stripe_plan_id}],
                )

                # Deactivate the user's old subscription
                UserSubscription.objects.filter(user=request.user, is_active=True).update(is_active=False)

                # Store the subscription details in your database
                UserSubscription.objects.create(
                    user=request.user,
                    plan=plan,
                    stripe_subscription_id=subscription.id,
                    start_date=timezone.now(),
                    end_date=timezone.now() + plan.duration,
                    is_active=True,  # Set the new subscription as active
                )

                return redirect('payments:success_page')

            except stripe.error.StripeError as e:
                # Handle Stripe exceptions
                form.add_error(None, str(e))

    else:
        if plan_id:
            initial_plan = SubscriptionPlan.objects.get(id=plan_id)
            form = BillingForm(initial={'subscription_plan': initial_plan})
        else:
            form = BillingForm()

    context = {
        'form': form,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'payments/billing.html', context)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return JsonResponse({'status': 'invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return JsonResponse({'status': 'invalid signature'}, status=400)

    # Handle the event
    if event.type == 'invoice.payment_succeeded':
        # Handle successful payment
        handle_successful_payment(event.data.object)
    elif event.type == 'invoice.payment_failed':
        # Handle failed payment
        handle_failed_payment(event.data.object)

    return JsonResponse({'status': 'success'})

def handle_successful_payment(invoice):
    # Get the subscription ID from the invoice
    subscription_id = invoice['subscription']

    # Get the UserSubscription with the matching Stripe subscription ID
    user_subscription = UserSubscription.objects.get(stripe_subscription_id=subscription_id)

    # Update the UserSubscription status
    user_subscription.is_active = True
    user_subscription.save()

def handle_failed_payment(invoice):
    # Get the subscription ID from the invoice
    subscription_id = invoice['subscription']

    # Get the UserSubscription with the matching Stripe subscription ID
    user_subscription = UserSubscription.objects.get(stripe_subscription_id=subscription_id)

    # Update the UserSubscription status
    user_subscription.is_active = False
    user_subscription.save()

def success_page(request):
    return render(request, 'payments/success.html')