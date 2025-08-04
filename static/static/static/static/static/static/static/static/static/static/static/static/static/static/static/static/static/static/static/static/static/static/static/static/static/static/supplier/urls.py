from django.urls import path
from . import views 
from django.conf import settings

urlpatterns = [
    path('', views.suppliers, name = 'SUPPLIERS'),
    path('supplier/<int:pk>/', views.supplier_detail, name = 'SUPPLIER_DETAIL')
    ]


#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)