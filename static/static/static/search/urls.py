from django.urls import path
from . import views 
from django.conf import settings

urlpatterns = [
    path('', views.search_item, name = 'SEARCH'),
    path('category/', views.category_detail, name = 'CAT_DETAILS'),
    ]