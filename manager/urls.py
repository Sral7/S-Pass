from django.urls import path
from . import views

appname ='manager'

urlpatterns =[
    path('<str:username>/add_site/', views.add_site, name='add_site'),
    path('<str:username>/settings/change_passcode', views.change_pass, name ='change_passcode'),
    path('<str:username>/settings/change_pin', views.change_pin, name ='change_pin'),
    path('<str:username>/settings/',views.user_settings, name ='settings'),
    path('<str:username>/Generate_Password/', views.generate_password, name='generate_password'),
    path('<str:username>/delete_site/<int:entry_id>/', views.delete_site, name='delete_site'),
    path('<str:username>/edit_site/<int:entry_id>/', views.edit_site, name='edit_site'),
    path('logout/', views.logout_manager, name ='logout'),
    path('<str:username>/', views.manager_display, name = 'password_manager'),
]