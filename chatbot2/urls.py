# chatbot2/urls.py

from django.urls import path
from .views import ChatBotAPIView, chat_view

urlpatterns = [
    path('chat/', ChatBotAPIView.as_view(), name='chatbot'),
    path('', chat_view, name='chat_view'), 
]

