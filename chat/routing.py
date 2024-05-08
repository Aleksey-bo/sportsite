from django.urls import path
from .consumer import ChatConsumer

websocket_urlpatterns = [
    path("", ChatConsumer.as_asgi()),
]
