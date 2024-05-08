from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Info', {
            'fields': ('phone_number', 'avatar'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
