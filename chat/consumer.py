import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Room, Message
from account.models import CustomUser


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        self.send_message_history()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_data = text_data_json['user']
        room_id = text_data_json['room']
        message = text_data_json["message"]

        user = CustomUser.objects.get(id=user_data)
        room = Room.objects.get(unique_id=room_id)

        Message.objects.create(user=user, room=room, content=message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat_message", "user": user_data, "room": room_id, "message": message
                }
        )
    
    def chat_message(self, event):
        user = event["user"]
        room = event["room"]
        message = event["message"]
        self.send(text_data=json.dumps({"user": user, "room": room, "message": message}))

    def send_message_history(self):
        messages = Message.objects.filter(room__unique_id=self.room_name)

        for message in messages:
            self.send(text_data=json.dumps({
                "user": message.user.id,
                "room": message.room.id,
                "message": message.content,
            }))