from django.urls import path
from . import views



urlpatterns =[
    path('', views.LoginScreen.as_view(), name='login'),
    path('<str:username>/create_pin', views.create_pin, name ='create_pin'),
    path('register/', views.register, name='register_user'),
    path('<str:username>/Decryption', views.enter_pin, name='decryption_pin')
]