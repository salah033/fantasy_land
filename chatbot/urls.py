from django.urls import path
from . import views 

urlpatterns = [
    path('', views.chatbot, name = 'CHATBOT'),
    #path('ask/', views.chatbot_ask, name='CHAT_BOT_ASK'),
    ]