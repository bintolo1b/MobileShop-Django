from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.store.models import Store

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=10, null=False)
    address = models.TextField(blank=True)

    class Meta:
        db_table = "CustomUser"

class Client(models.Model):
    username = models.OneToOneField(CustomUser, on_delete=models.PROTECT, to_field='username', db_column='username')
    class Meta:
        db_table = "client"
    def __str__(self):
        return self.username.username

class Staff(models.Model):
    username = models.OneToOneField(CustomUser, on_delete=models.PROTECT, to_field='username', db_column='username')
    level = models.CharField(max_length=50, null=False, blank=False)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    class Meta:
        db_table = "staff"

class ShopOwner(models.Model):
    username = models.OneToOneField(CustomUser, on_delete=models.PROTECT, to_field='username', db_column='username')
    class Meta:
        db_table = "shopowner"
