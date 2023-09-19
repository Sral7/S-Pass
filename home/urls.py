from django.urls import path
from . import views

urlpatterns =[
    path('',views.homeScreen, name='home_screen'),
]

