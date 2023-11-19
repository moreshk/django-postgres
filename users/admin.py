from django.contrib import admin
from .models import CustomUser,  GlobalSettings  

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

@admin.register(SampleTopic)
class SampleTopicAdmin(admin.ModelAdmin):
    readonly_fields = ('creator',)

    def save_model(self, request, obj, form, change):
        if not change:  # Only set creator during the first save.
            obj.creator = request.user
        super().save_model(request, obj, form, change)

@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = ('referring_user_bonus', 'referred_user_bonus')