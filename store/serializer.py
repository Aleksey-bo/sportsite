from rest_framework import serializers
from .models import (
    Category,
    Product,
    Image,
    City
)
from account.serializer import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'category_name', 'image')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('url',)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'location']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    location_product = CitySerializer()
    image = ImageSerializer(many=True, required=False)
    user = UserSerializer()

    class Meta:
        model = Product
        fields = ('id', 'title', 'category', 'user', 'description', 'location_product', 'image', 'price', 'active')


class ProductCreateSerializer(serializers.ModelSerializer):
    image = serializers.ListField(child=serializers.ImageField(), write_only=True, required=False)

    class Meta:
        model = Product
        fields = ('title', 'category', 'user', 'description', 'location_product', 'price', 'active', 'image')

    def create(self, validated_data):
        images_data = validated_data.pop('image', [])
        product = Product.objects.create(**validated_data)
        for image_data in images_data:
            image = Image.objects.create(url=image_data)
            product.image.add(image)
        return product

    def update(self, instance, validated_data):
        pass
