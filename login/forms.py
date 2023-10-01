from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']

class PinForm(forms.Form):

    pin = forms.CharField(
        label='Enter PIN:',
        min_length=4,  # You can specify the minimum and maximum lengths
        max_length=8,  # for your PIN here.
        widget=forms.TextInput(attrs={'type': 'number','id':'pin'}),
    )
    confirm_pin = forms.CharField(
        label='Confirm PIN:',
        min_length=4,
        max_length=8,
        widget=forms.TextInput(attrs={'type': 'number','id':'confirm_pin'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data['pin']
        confirm_pin = cleaned_data['confirm_pin']
        if pin != confirm_pin:
            raise forms.ValidationError('PIN codes do not match')

