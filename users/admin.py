from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'last_login')
    search_fields = ('email',)  # Note the comma to make it a tuple
    ordering = ('email',)  # Note the comma to make it a tuple

admin.site.register(CustomUser, CustomUserAdmin)
