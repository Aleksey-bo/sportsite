from rest_framework import serializers
from .models import (
    Category,
    Product,
    Image,
    City
)
from account.serializer import UserSerializer
from account.models import CustomUser


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

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        location_data = validated_data.pop('location_product')
        images_data = validated_data.pop('image', None)
        user_data = validated_data.pop('user')

        category = Category.objects.get(category_name=category_data.get('category_name'))
        location = City.objects.get(location=location_data.get('location'))
        user = CustomUser.objects.get(id=user_data)

        product = Product.objects.create(category=category, location_product=location, user=user, **validated_data)

        if images_data:
            for image_data in images_data:
                image = Image.objects.create(image_data)
                product.image.add(image)

        return product
