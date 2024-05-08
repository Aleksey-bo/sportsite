from rest_framework.serializers import ModelSerializer
from .models import (
    Category,
    Product,
    Image,
    City
)


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ImageSerializer(ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class CitySerializer(ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    image = ImageSerializer(many=True)
    category = CategorySerializer()
    location_product = CitySerializer()

    class Meta:
        model = Product
        fields = [
            'id', 'user', 'title', 'category', 'description', 'image', 'location_product', 'price', 'active', 'date'
        ]
        read_only_fields = ['id', 'category']
