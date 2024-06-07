import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import Q
from django.db.models.signals import post_save
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

        msg = Message.objects.create(user=user, room=room, content=message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat_message", "user": user_data, "room": room_id, "message": message
                }
        )
    
    def chat_message(self, event):
        self.send(text_data=json.dumps({
            "user": event["user"], "room": event["room"], "message": event["message"]
            }))

    def send_message_history(self):
        messages = Message.objects.filter(room__unique_id=self.room_name)
        message_list = []

        for message in messages:
            message_list.append({
                "user": message.user.username,
                "room": message.room.id,
                "message": message.content,
            })

        self.send(text_data=json.dumps({"message_history": message_list}))


class NotificationChat(WebsocketConsumer):
    def connect(self):
        self.username = self.scope["url_route"]["kwargs"]["username"]
        self.accept()

        post_save.connect(self.send_notification, sender=Message)

    def disconnect(self, code):
        pass

    def send_notification(self, **kwargs):
        user = CustomUser.objects.get(username=self.username)
        rooms = Room.objects.filter(Q(seller=user.id) | Q(client=user.id))
        notification_list = []

        for room in rooms:
            message = Message.objects.filter(room=room.id).last()

            if user.id != message.user.id:
                notification_list.append({"user": message.user.username, "room": message.room.id, "message": message.content})

        notification_count = len(notification_list)
        self.send(text_data=json.dumps({"notification_count": notification_count, "last_message": notification_list}))
            

