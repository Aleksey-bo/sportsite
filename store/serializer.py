from rest_framework import serializers
from .models import (
    Category,
    Product,
    Image,
    City
)


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
        fields = ('id', 'location')


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    location_product = CitySerializer()
    image = ImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ('id', 'title', 'category', 'user', 'description', 'location_product', 'image', 'price', 'active')

    def create(self, validated_data):
        print(validated_data)
        category_data = validated_data.pop('category')
        location_data = validated_data.pop('location_product')
        images_data = validated_data.pop('image', None)

        category = Category.objects.get(category_name=category_data.get('category_name'))
        location = City.objects.get(location=location_data.get('location'))

        image = ImageSerializer(**images_data)
        product = Product.objects.create(category=category, location_product=location, image=image, **validated_data)

        return product
