from django.contrib import admin
from .models import CustomUser, Client, Staff, ShopOwner
# Register your models here.

admin.site.register([CustomUser, Client, Staff, ShopOwner])