from .models import User
from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['gender', 'is_active']
