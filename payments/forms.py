from django import forms
from .models import SubscriptionPlan

class BillingForm(forms.Form):
    cardholder_name = forms.CharField(max_length=100, label="Cardholder Name")
    subscription_plan = forms.ModelChoiceField(queryset=SubscriptionPlan.objects.all(), label="Subscription Plan")
    stripe_token = forms.CharField(widget=forms.HiddenInput())  # This will store the Stripe token
