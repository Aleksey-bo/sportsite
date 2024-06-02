from uuid import uuid4
from typing import Iterable
from django.db import models
from django.conf import settings


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=20, null=False)
    image = models.FileField(upload_to='img_category/', blank=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=64)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=False)
    description = models.CharField(max_length=512)
    image = models.ManyToManyField('Image', blank=True)
    location_product = models.ForeignKey('City', on_delete=models.CASCADE, null=False)
    price = models.FloatField()
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    url = models.ImageField(upload_to="")


class City(models.Model):
    location = models.CharField(max_length=20)

    def __str__(self):
        return self.location


class Order(models.Model):
    unique_id = models.CharField(max_length=64)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now=False)
    end_date = models.DateTimeField(auto_now=False)
    pay = models.BooleanField(default=False)
    bill = models.FileField(upload_to='bill/', null=False)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.unique_id}"

