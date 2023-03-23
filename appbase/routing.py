from django.urls import path 
from . import consumers


websocket_urlpatterns = [
    path('room/<str:pk>/', consumers.ChatConsumer.as_asgi()),
]
