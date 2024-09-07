# urls.py
from django.urls import path
from .views import chatbot_view

urlpatterns = [
    path('chat/', chatbot_view, name='chat'),
]
