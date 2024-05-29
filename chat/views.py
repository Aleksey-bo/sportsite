from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room
from account.models import CustomUser


# Create your views here.
class RoomView(APIView):
    def post(self, request):
        product = request.data.get('product')
        seller = request.data.get('seller')
        client = request.data.get('client')

        room = Room.objects.filter(product=product, users__id__in=(seller, client)).first()
        return Response({"id": room.id, "unique_id": room.unique_id})