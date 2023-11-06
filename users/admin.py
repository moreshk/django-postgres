from django.contrib import admin
from .models import CustomUser 

from v3essay_grader.models import SampleTopic
from payments.models import UserSubscription

class UserSubscriptionInline(admin.TabularInline):
    model = UserSubscription
    extra = 0

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    inlines = [UserSubscriptionInline]

admin.site.register(SampleTopic)