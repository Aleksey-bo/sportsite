from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .permission import IsAuthenticatedOrCreateOnly
from .models import (
    Product,
    Category
)
from .serializer import (
    ProductSerializer,
    CategorySerializer
)


# Create your views here.
class ListCategory(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductsView(ModelViewSet):
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductSerializer

# class ProductsView(ViewSet):
#     @staticmethod
#     def list(request):
#         products = Product.objects.filter(active=True)
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
#
#     @staticmethod
#     def retrieve(request, pk=None):
#         products = Product.objects.filter(id=pk, active=True)
#         serializer = ProductSerializer(products)
#         return Response(serializer.data)
#
#     def create(self):
#         pass
#
#     def update(self, request, pk=None):
#         pass
#
#     def destroy(self, request, pk=None):
#         pass
