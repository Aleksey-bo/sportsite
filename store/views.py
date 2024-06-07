from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .permission import IsAuthenticatedOrCreateOnly
from store.pagination import Pagination
from .models import (
    Product,
    Category,
    City,
    Order
)
from .serializer import (
    ProductSerializer,
    ProductCreateSerializer,
    CategorySerializer,
    CitySerializer,
    OrderSerializer
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
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title']
    filterset_fields = ['category__category_name']
    pagination_class = Pagination
    permission_classes = [IsAuthenticatedOrCreateOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'destroy']:
            return ProductCreateSerializer
        return self.serializer_class
    

class OrderView(ListAPIView, CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action in ['create']:
            queryset = Order.objects.all()

        user_id = self.request.user
        queryset = Order.objects.filter(user=user_id.id, pay=True)
        return queryset
    
