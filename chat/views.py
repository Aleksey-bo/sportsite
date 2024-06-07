from uuid import uuid4
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Room
from account.models import CustomUser
from store.models import Product


# Create your views here.
class RoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_data = request.data.get('product', None)
        seller_data = request.data.get('seller', None)
        client_data = request.data.get('client', None)

        room = Room.objects.filter(product=product_data, seller=seller_data, client=client_data).first()

        if not room:
            product = Product.objects.get(id=product_data)
            seller = CustomUser.objects.get(id=seller_data)
            client = CustomUser.objects.get(id=client_data)
            unique_id = uuid4().hex
            room = Room.objects.create(unique_id=unique_id, product=product, seller=seller, client=client)
            return Response({"id": room.id, "unique_id": room.unique_id})
        
        return Response({
            "id": room.id,
              "unique_id": room.unique_id,
                "seller": room.seller.id,
                  "client": room.client.id
                  })