from django.db import models

# Create your models here.
class Users(models.Model):
    user = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.user

class Data(models.Model):
    password = models.CharField(max_length=300)

    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.password
