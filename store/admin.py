from django.contrib import admin
from .models import (
    Category,
    Product,
    City,
    Image,
    Order
)

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(City)
admin.site.register(Image)
admin.site.register(Order)
