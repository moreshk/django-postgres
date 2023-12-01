from django.db import models

# Create your models here.
# translator/models.py

from users.models import CustomUser

class Translation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    english_text = models.TextField()
    LANGUAGE_CHOICES = (
        ('English', 'English'),
        ('Marathi', 'Marathi'),
        ('Gujarati', 'Gujarati'),
        ('Hindi', 'Hindi'),
    )
    translated_language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    translated_text_user_input = models.CharField(max_length=500)
    admin_comment = models.TextField(null=True, blank=True)
    STATUS_CHOICES = (
        ('Submitted', 'Submitted'),
        ('Reviewed', 'Reviewed'),
        ('Accepted', 'Accepted'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Submitted')