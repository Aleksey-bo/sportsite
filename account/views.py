from django.db.models import Q
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import (
    RegisterSerializer,
    UserSerializer
)
from store.serializer import ProductSerializer
from store.models import Product
from chat.serializer import RoomSerializer
from chat.models import Room


# Create your views here.
class RegistrationAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(tokens, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCurrentUser(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        return Response(UserSerializer(request.user).data)

    @staticmethod
    def put(request):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class GetUserProduct(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Product.objects.filter(user=user_id)
        return queryset


class GetUserChat(ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Room.objects.filter(Q(seller=user_id) | Q(client=user_id))
        return queryset.order_by('-id')