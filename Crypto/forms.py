# forms.py
from django import forms
from .models import UserDetails, UserIdentity
from .models import CryptoAsset


class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'date_of_birth', 'identity']

    def save(self, commit=True):
        instance = super().save(commit=False)
        identity = self.cleaned_data.get('identity', None)

        if identity:
            instance.identity_uploaded = True

        if commit:
            instance.save()
        return instance
class IdentityUploadForm(forms.ModelForm):
    class Meta:
        model = UserIdentity
        fields = ['identity_uploaded', 'identity_photo']

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