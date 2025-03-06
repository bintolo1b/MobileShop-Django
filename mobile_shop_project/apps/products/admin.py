from django.contrib import admin

# Register your models here.
from .models import Phone, Product, Category, PhoneConfiguration, PhoneVariant

admin.site.register([Phone, Product, Category, PhoneConfiguration, PhoneVariant])
