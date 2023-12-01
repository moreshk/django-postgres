# translator/forms.py

from django import forms
from .models import Translation

class TranslationForm(forms.ModelForm):
    class Meta:
        model = Translation
        fields = ['translated_language', 'translated_text_user_input']

    def __init__(self, *args, **kwargs):
        super(TranslationForm, self).__init__(*args, **kwargs)
        # Add any custom form initialization here