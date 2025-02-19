from django.db import models
from apps.users.models import Client
from apps.products.models import Product
# Create your models here.
class Cart(models.Model):
    client = models.OneToOneField(Client, on_delete = models.PROTECT)
    class Meta:
        db_table = "cart"

class Cart_Product(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.PROTECT)
    product = models.ForeignKey(Product, on_delete = models.PROTECT)
    quantity = models.IntegerField(null=False)

    class Meta:
        db_table = "cart_product"
        constraints = [
            models.UniqueConstraint(fields=['cart', 'product'], name='unique_cart_product')
        ]