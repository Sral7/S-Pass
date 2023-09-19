from django.shortcuts import render
from .models import Users,Data
from django.contrib.auth.views import LoginView

# Create your views here.

def homeScreen(request):
    users = Users.objects.all()
    data = Data.objects.all()
    context ={
        'users': users,
        'data':data
    }

    return render(request, 'home/home_screen.html',context)





