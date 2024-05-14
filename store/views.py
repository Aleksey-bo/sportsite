from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import filters
from .permission import IsAuthenticatedOrCreateOnly
from server.pagination import Pagination
from .models import (
    Product,
    Category,
    City
)
from .serializer import (
    ProductSerializer,
    ProductCreateSerializer,
    CategorySerializer,
    CitySerializer
)


# Create your views here.
class ListCategory(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ListCity(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]


class ProductsView(ModelViewSet):
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = Pagination


    def get_serializer_class(self):
        if self.action == 'create':
            return ProductCreateSerializer
        return self.serializer_class

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
