from django.db import models
from hashlib import sha512
import secrets
from django.contrib.auth.hashers import make_password,check_password

# Create your models here.
class userProfile(models.Model):

    user = models.CharField(max_length=18, unique=True)
    hashed_pin = models.CharField(max_length=128, default='')
    salt = models.BinaryField(default=b'\x00' * 16)

    def save(self, *args, **kwargs):
        if not self.salt  or self.salt == b'\x00' * 16:
            self.salt = secrets.token_bytes(16)
        super().save(*args, **kwargs)

    
    def hash_pin(self,pin):
        salted_pin = bytes(self.salt) + pin.encode()
        self.hashed_pin = make_password(salted_pin)

    def check_pin(self,pin):
        salted_pin = self.salt + pin.encode()
        return check_password(salted_pin,self.hashed_pin)
    
    def __str__(self) -> str:
        return self.user

