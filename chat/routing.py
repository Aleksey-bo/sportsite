from django.urls import re_path
from .consumer import (
    ChatConsumer,
    NotificationChat
)

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/notification/(?P<username>\w+)/$", NotificationChat.as_asgi())
]
