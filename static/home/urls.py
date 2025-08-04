from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home_redirect, name = 'home_redirect'),
    path('home/', views.home_page, name = 'HOME'),
    path('home/about/', views.about_page, name = 'ABOUT'),
    path('filter-low-stock/', views.filter_low_stock, name='filter_low_stock'),
    path('filter-best-seller/', views.filter_best_seller, name='filter_best_seller'),
    ]

