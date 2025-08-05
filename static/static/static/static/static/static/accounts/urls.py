from django.urls import path
from . import views 

urlpatterns = [
    path('', views.accounts_home, name = 'ACCOUNTS_HOME'),   
    path('login/', views.accounts_login, name = 'ACCOUNTS_LOGIN'),    
    path('register/', views.accounts_register, name = 'ACCOUNTS_REGISTER'),
    path('logout/', views.accounts_logout, name='ACCOUNTS_LOGOUT'),   
    path('dashboard/', views.user_dashboard, name='USER_DASHBOARD')
    ]