from rest_framework import serializers
from .models import (
    Category,
    Product,
    Image,
    City,
    Order
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
        images_data = validated_data.pop('image', [])

        instance.title = validated_data.get('title', instance.title)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description', instance.description)
        instance.location_product = validated_data.get('location_product', instance.location_product)
        instance.price = validated_data.get('price', instance.price)
        instance.active = validated_data.get('active', instance.active)
        instance.save()

        if images_data:
            instance.image.clear()
            for image_data in images_data:
                image = Image.objects.create(url=image_data)
                instance.image.add(image)
        
        return instance


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'unique_id', 'user', 'product', 'start_date', 'end_date', 'pay', 'bill']
        read_only_fields = ['id', 'bill']

    def create(self, validated_data):
        product = Product.objects.get(title=validated_data.get('product'))
        order = Order.objects.create(**validated_data)
        
        if order and product:
            product.active = False
            product.save()

        return order