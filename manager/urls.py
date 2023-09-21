from django.urls import path
from . import views

appname ='manager'

urlpatterns =[
    path('<str:username>/add_site/', views.add_site, name='add_site'),
    path('<str:username>/settings/',views.user_settings, name ='settings'),
    path('<str:username>/edit_site/<int:entry_id>/', views.edit_site, name='edit_site'),
    path('logout/', views.logout_manager, name ='logout'),
    path('<str:username>/', views.manager_display, name = 'password_manager'),
]