from django.urls import path
from .views import RoomView

urlpatterns = [
    path('get_room/', RoomView.as_view(), name='registration'),
]