import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        pass

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def sendMessage(self, event):
        pass
