from typing import Any
from .models import userData,userProfile
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

class dataForm(forms.ModelForm):

    username = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'id':'output'}))

    class Meta:
        model = userData
        fields = ['site','url']

class editForm(forms.Form):
    site = forms.CharField(max_length=255, required=True)
    url = forms.URLField(required=True)
    dec_username = forms.CharField(max_length=255, required=True,label='Username')
    dec_email = forms.EmailField(required=True,label='Email')
    dec_password = forms.CharField(max_length=255,required=True,label='Password', widget=forms.TextInput(attrs={'id':'output'}))

class editPasscode(forms.Form):

    pin = forms.CharField(min_length=4, max_length= 8, widget=forms.TextInput(attrs={'type':'number'}))

    new_password1 = forms.CharField(max_length=40,label='New Password', 
                                    strip=True,
                                    widget= forms.PasswordInput(attrs={'autocomplete':'new-password'}))
        
    new_password2 = forms.CharField(max_length=40, label='Confirm Passcode', strip=True,
                                    widget=forms.PasswordInput(attrs={'autocomplete':'new-password'}))
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__( *args, **kwargs)
        self.user = user
    
    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get('pin')
        pass1 = cleaned_data.get('new_password1')
        pass2 = cleaned_data.get('new_password2')
        user_profile = userProfile.objects.get(user = self.user)

        if pass1 != pass2:
            raise forms.ValidationError('PASSWORDS DO NO MATCH')

        if not user_profile.check_pin(pin):
            raise forms.ValidationError('INCORECT PIN')
        
class editPin(forms.Form):
    new_pin = forms.CharField(label='New PIN:',min_length=4, max_length=8,widget=forms.TextInput(attrs={'type':'number'}))
    confirm_pin = forms.CharField(label='Confirm Pin',min_length=4, max_length=8,widget=forms.TextInput(attrs={'type':'number'}))

    passcode = forms.CharField(max_length=40, label='Confirm Passcode', strip=True,
                                    widget=forms.PasswordInput(attrs={'autocomplete':'new-password'})) 
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        pin1 = cleaned_data.get('new_pin')   
        pin2 = cleaned_data.get('confirm_pin') 
        passcode = cleaned_data.get('passcode')
        user = User.objects.get(username= self.user)
        if pin1 != pin2:
            raise forms.ValidationError('PINS DO NOT MATCH')
        if not check_password(passcode,user.password):
            raise forms.ValidationError('INCORRECT PASSWORD')
        
        




        

        
    

    



    
