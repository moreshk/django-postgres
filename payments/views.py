import stripe
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import BillingForm
from .models import UserSubscription
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def billing(request):
    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            # Use Stripe SDK to create a new subscription or update billing details
            token = form.cleaned_data['stripe_token']
            plan = form.cleaned_data['subscription_plan']

            try:
                # Assuming you have a Stripe Customer ID stored for the user
                customer_id = request.user.stripe_customer_id

                # Create a new subscription using Stripe SDK
                subscription = stripe.Subscription.create(
                    customer=customer_id,
                    items=[{'plan': plan.stripe_plan_id}],  # This assumes you have a stripe_plan_id field in your SubscriptionPlan model
                    source=token,
                )

                # Store the subscription details in your database
                UserSubscription.objects.create(
                    user=request.user,
                    plan=plan,
                    stripe_subscription_id=subscription.id,
                    start_date=timezone.now(),
                    end_date=timezone.now() + plan.duration,
                )

                return redirect('success_page')  # Redirect to a success page or wherever you want

            except stripe.error.StripeError as e:
                # Handle Stripe exceptions
                form.add_error(None, str(e))

    else:
        form = BillingForm()

    context = {
            'form': form,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        }
    return render(request, 'payments/billing.html', context)
    # return render(request, 'payments/billing.html', {'form': form})




stripe.api_key = settings.STRIPE_SECRET_KEY

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
    if event.type == 'invoice.paid':
        # Handle successful payment
        pass
    elif event.type == 'invoice.payment_failed':
        # Handle failed payment
        pass
    # ... handle other event types as needed

    return JsonResponse({'status': 'success'})
