from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializer import (
    RegisterSerializer,
    UserSerializer
)


# Create your views here.
class CreateUserView(CreateAPIView):
    queryset = get_user_model()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class GetCurrentUser(APIView):

    @staticmethod
    def get(request):
        return Response(UserSerializer(request.user).data)

    def put(self):
        pass

    def destroy(self):
        pass

