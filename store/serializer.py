from uuid import uuid4
from rest_framework import serializers
from .models import (
    Category,
    Product,
    Image,
    City,
    Order
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
        fields = ('id', 'location')


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
        user_data = validated_data.pop('user', {})
        product = Product.objects.filter(id=validated_data.get('id'))
        category = Category.objects.filter(id=validated_data.get('category'))
        city = City.objects.filter(id=validated_data.get('location_product'))

        if product.user.id == user_data.get('id'):
            instance.title = validated_data.get('title')
            instance.description = validated_data.get('description')
            if category:
                instance.category = category
            if city:
                instance.location_product = city

            instance.price = validated_data.get('price')
            instance.active = validated_data.get('active')

            instance.save()

        return instance


class OrderSerializer(serializers.ModelSerializer):
    unique_id = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'unique_id', 'user', 'product', 'start_date', 'end_date', 'pay', 'bill']

    def create(self, validated_data):
        order = Order.objects.create(unique_id=uuid4(), **validated_data)
        product = Product.objects.get(title=validated_data.get('product'))

        if order and product:
            product.active = False
            product.save()

        return order