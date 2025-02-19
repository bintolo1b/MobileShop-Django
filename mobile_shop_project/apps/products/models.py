from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        db_table = "category"

class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    brand = models.CharField(max_length=100, null=False, blank=False)   
    price = models.FloatField(null=False)
    stock_quantity = models.IntegerField(null=False)
    status = models.CharField(max_length=50, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    class Meta:
        db_table = "product"

class Phone(Product):
    screen = models.TextField(blank=True)
    cpu = models.TextField(blank=True)
    rom = models.TextField(blank=True)
    ram = models.TextField(blank=True)
    front_camera = models.TextField(blank=True)
    back_cammera = models.TextField(blank=True)
    battery = models.TextField(blank=True)
    charger = models.TextField(blank=True)
    speaker = models.TextField(blank=True)

    class Meta:
        db_table = "phone"



