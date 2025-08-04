from django.urls import path
from . import views 
from django.conf import settings

urlpatterns = [
    path('', views.products, name = 'PRODUCTS'),
    path('product/<int:pk>/', views.product_detail, name = 'PRODUCT_DETAIL'),
    ]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)