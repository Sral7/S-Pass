from django.urls import path
from . import views

appname ='manager'

urlpatterns =[
    path('<str:username>/add_site/', views.add_site, name='add_site'),
    path('logout/', views.logout_manager, name ='logout'),
    path('<str:username>/', views.manager_display, name = 'password_manager'),
]