from uuid import uuid4
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Room
from account.models import CustomUser


# Create your views here.
class RoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_data = request.data.get('product', None)
        seller_data = request.data.get('seller', None)
        client_data = request.data.get('client', None)

        room = Room.objects.filter(product=product_data, seller=seller_data, client=client_data).first()

        if not room:
            room = Room.objects.create(unique_id=uuid4(), users=(seller_data,client_data))
            return Response({"id": room.id, "unique_id": room.unique_id})
        
        return Response({"id": room.id, "unique_id": room.unique_id})