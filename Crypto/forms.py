# forms.py
from django import forms
from .models import UserDetails

class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'date_of_birth']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
