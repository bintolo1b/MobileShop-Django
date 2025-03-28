from django.db import models

# Create your models here.
class Store(models.Model):
    address = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.address

    class Meta:
        db_table = "store"


