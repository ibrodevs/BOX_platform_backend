from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_message, name='send_message'),
    path('history/', views.get_chat_history, name='chat_history'),
    path('clear/', views.clear_chat_history, name='clear_chat'),
]
