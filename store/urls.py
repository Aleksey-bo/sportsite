from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ListCategory,
    ListCity,
    ProductsView,
    OrderView
)

router = DefaultRouter()
router.register(r'products', ProductsView, basename='products')

urlpatterns = [
    path('get_category/', ListCategory.as_view()),
    path('get_city/', ListCity.as_view()),
    path('order/', OrderView.as_view()),
    path('', include(router.urls))
]

