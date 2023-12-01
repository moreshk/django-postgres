from django.contrib import admin

# Register your models here.
# translator/admin.py

from .models import Translation

admin.site.register(Translation)