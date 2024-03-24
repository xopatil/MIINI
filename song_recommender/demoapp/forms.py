from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser 

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    # Your additional form validation or customization can go here
