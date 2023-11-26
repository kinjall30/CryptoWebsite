# forms.py
from django import forms
from .models import UserDetails
from .models import CryptoAsset

class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'date_of_birth']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class FieldSelectionForm(forms.Form):
    fields_choices = [
        ('name', 'Name'),
        ('price', 'Price'),
        ('high', 'High (24h)'),
        ('low', 'Low (24h)'),
        ('price_change_24h', 'Price Change (24h)'),
        ('price_change_percentage_24h', 'Price Change (%) (24h)'),
        ('market_cap', 'Market Cap'),
        ('volume_24h', 'Volume (24h)'),
        ('circulating_supply', 'Circulating Supply'),
    ]

    field_selection = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=fields_choices,
    )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'date_of_birth']