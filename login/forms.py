from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

class CustomAuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Please enter a correct username and password combination.',
    }
    


class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
        

class PinForm(forms.Form):

    pin = forms.CharField(
        label='Enter PIN:',
        widget=forms.TextInput(attrs={'type': 'number','id':'pin'}),
    )
    confirm_pin = forms.CharField(
        label='Confirm PIN:',
        widget=forms.TextInput(attrs={'type': 'number','id':'confirm_pin'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data['pin']
        confirm_pin = cleaned_data['confirm_pin']
        if pin != confirm_pin:
            self.add_error('confirm_pin','PINs Do Not Match')
        if len(pin) < 4:
            self.add_error('pin','PIN Must Be At Least 4 Characters Long')
        if len(pin) > 8:
            self.add_error('pin','PIN Must Be At Most 8 Characters Long')

