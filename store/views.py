from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
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
    permission_classes = [IsAuthenticatedOrCreateOnly]
