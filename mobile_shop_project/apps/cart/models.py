from django.db import models
from apps.users.models import Client
from apps.products.models import PhoneVariant
# Create your models here.
class Cart(models.Model):
    client = models.OneToOneField(Client, on_delete = models.PROTECT)
    class Meta:
        db_table = "cart"

class Cart_PhoneVariant(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.PROTECT)
    phone_variant = models.ForeignKey(PhoneVariant, on_delete = models.PROTECT)
    quantity = models.IntegerField(null=False)

    class Meta:
        db_table = "cart_phone_variant"
        constraints = [
            models.UniqueConstraint(fields=['cart', 'phone_variant'], name='unique_cart_variant')
        ]