from django import forms

from .models import User


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone', 'address', 'telegram_id', 'bio', 'district', 'image', 'type']
