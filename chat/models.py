from django.db import models
from django.conf import settings
from store.models import Product

# Create your models here.
class Room(models.Model):
    unique_id = models.CharField(max_length=32)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self) -> str:
        return f'{self.unique_id}'


class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=1024)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username}: {self.content} [{self.date}]"