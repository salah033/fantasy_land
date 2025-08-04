from django.urls import path
from . import views 

urlpatterns = [
    path('', views.shop_home, name = 'SHOP'),
    #path('ask/', views.chatbot_ask, name='CHAT_BOT_ASK'),
    ]