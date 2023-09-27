from typing import Any
from django.db import models
from login.models import userProfile
from django.contrib.sessions.models import Session
from cryptography.fernet import Fernet
import base64
# Create your models here.

class Websites(models.Model):
    url = models.URLField()
    user = models.ForeignKey(userProfile, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='icons/')




class userData(models.Model):
    
    user = models.ForeignKey(userProfile, on_delete=models.CASCADE)
    website = models.ForeignKey(Websites, on_delete=models.CASCADE, null=True, blank=True)
    enc_username = models.BinaryField(default=b'')
    enc_email = models.BinaryField(default=b'')
    enc_password = models.BinaryField(default=b'')
    site = models.CharField(max_length=255)
    url = models.URLField()
    cipher_suite = None

    def encyrpt_data(self,data):
        return self.cipher_suite.encrypt(data.encode())
    def decrypt_data(self,data):
        return self.cipher_suite.decrypt(data).decode() 
    
    def save(self, *args, **kwargs):
        if self.username:
            self.enc_username = self.encyrpt_data(self.username)
        if self.email:
            self.enc_email = self.encyrpt_data(self.email)
        if self.password:
            self.enc_password = self.encyrpt_data(self.password)
        
        self.website = Websites.objects.get(user= self.user,url =self.url)
        super().save(*args, **kwargs)
    
    def read_form(self,username,email,password,request):
        self.username = username
        self.email = email
        self.password = password
        self.cipher_suite = Fernet(base64.urlsafe_b64encode(base64.b64decode(request.session['KDFP'])))
    
    def decrypt_entry(self,request):
        self.cipher_suite = Fernet(base64.urlsafe_b64encode(base64.b64decode(request.session['KDFP'])))
        if self.cipher_suite:
            dec_email = self.decrypt_data(self.enc_email)
            dec_username= self.decrypt_data(self.enc_username)
            dec_password = self.decrypt_data(self.enc_password)
        return {'site': self.site, 'url':self.url, 'dec_username':dec_username, 'dec_email':dec_email, 'dec_password':dec_password}
    
    @classmethod
    def filter_decrypt(cls,request,**kwargs):
        queryset = cls.objects.filter(**kwargs)
        cls.cipher_suite = Fernet(base64.urlsafe_b64encode(base64.b64decode(request.session['KDFP'])))
        for obj in queryset:
            obj.username = cls.decrypt_data(obj,obj.enc_username)
            obj.email = cls.decrypt_data(obj,obj.enc_email)
            obj.password = cls.decrypt_data(obj,obj.enc_password)
        return queryset


        




