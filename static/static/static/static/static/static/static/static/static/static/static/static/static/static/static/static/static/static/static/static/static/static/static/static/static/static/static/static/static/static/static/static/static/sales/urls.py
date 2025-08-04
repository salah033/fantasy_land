from django.urls import path
from . import views 

urlpatterns = [
    path('', views.sale_page, name = 'MAKE_SALE'),
    path('ajax/get-product/', views.get_product_by_barcode, name='GET_PRODUCT_BY_BARCODE'),
    path('ajax/confirm-sale/', views.confirm_sale, name='CONFIRM_SALE'),
    path('receipt/<int:sale_id>/', views.sale_receipt, name='SALE_RECEIPT'),
    path('all_reciepts/', views.all_receipts, name= 'ALL_RECEIPTS'),
    path('close_drawer/', views.close_drawer, name= 'CLOSE_DRAWER'),
    path('close_drawer/confirmed', views.close_confirmed, name= 'CLOSE_DRAWER_CON' ),
    ]