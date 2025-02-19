from django.db import models
from apps.users.models import Client
from apps.products.models import Product
from apps.users.models import Staff
from apps.store.models import Store
# Create your models here.
class Order(models.Model):
    payment_method = models.CharField(max_length=50, blank=False, null=False)
    client_phone = models.CharField(max_length=10)
    time = models.TimeField()
    staff_in_charge = models.ForeignKey(Staff, on_delete=models.PROTECT)
    class Meta:
        db_table = "order"


class Client_Order(models.Model):
    client = models.ForeignKey(Client, on_delete = models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    class Meta:
        db_table = "client_order"
        constraints = [
            models.UniqueConstraint(fields=['client', 'order'], name='unique_client_order')
        ]

class DirectOrder(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    class Meta:
        db_table = "directorder"

class OnlineOrder(models.Model):
    shippong_address = models.TextField(max_length=300, null=False, blank=False)
    status = models.CharField(max_length=20, blank=False, null=False)
    payment_status = models.CharField(max_length=20, blank=False, null=False)
    class Meta:
        db_table = "onlineorder"

class Product_Order(models.Model):
    product = models.ForeignKey(Product, on_delete = models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    quantity = models.IntegerField(null=False)

    class Meta:
        db_table = "product_order"
        constraints = [
            models.UniqueConstraint(fields=['product', 'order'], name='unique_product_order')
        ]
    