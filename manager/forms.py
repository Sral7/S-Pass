from .models import userData
from django import forms

class dataForm(forms.ModelForm):

    username = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput)

    class Meta:
        model = userData
        fields = ['site']

class editForm(forms.Form):
    site = forms.CharField(max_length=255, required=True)
    dec_username = forms.CharField(max_length=255, required=True,label='Username')
    dec_email = forms.EmailField(required=True,label='Email')
    dec_password = forms.CharField(max_length=255,required=True,label='Password')


    
