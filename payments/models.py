from django.db import models
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()  # e.g., 30 days for a monthly plan
    description = models.TextField(null=True, blank=True)
    word_count_limit = models.IntegerField(null=True, blank=True)  # new field
    essay_limit = models.IntegerField(null=True, blank=True)  # new field
    stripe_plan_id = models.CharField(max_length=50)  # new field
    # ... any other fields like features, etc.

    def __str__(self):
        return self.name
    
class UserSubscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    stripe_subscription_id = models.CharField(max_length=50)  # ID from Stripe for this subscription
    # ... any other fields like payment method, etc.

class Payment(models.Model):
    user_subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    stripe_charge_id = models.CharField(max_length=50)
    # ... any other fields you find necessary
