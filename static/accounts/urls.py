from django.urls import path
from . import views 

urlpatterns = [
    path('', views.accounts_home, name = 'ACCOUNTS_HOME'),   
    path('login/', views.accounts_login, name = 'ACCOUNTS_LOGIN'),    
    path('register/', views.accounts_register, name = 'ACCOUNTS_REGISTER'),
    path('logout/', views.accounts_logout, name='ACCOUNTS_LOGOUT'),   
    path('dashboard/', views.user_dashboard, name='USER_DASHBOARD'),
    path('submit_form/', views.submit_user_note, name='SUBMIT_FORM'),
    path('memo/', views.memo_form, name="MEMO_FORM"), 
    path('show_memo/', views.show_memos, name='SHOW_MEMO'),
    path('memo_edit/<str:category>/<int:pk>/', views.edit_memo, name='EDIT_MEMO'),
    path('costumers/', views.show_costumers, name='COSTUMERS'),
    path('costumer/<int:pk>', views.customer_details, name='COSTUMER_DETAILS'),
    ]