from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    brand = models.CharField(max_length=100, null=False, blank=False)   
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

    def __str__(self):
        return self.name
    
class PhoneConfiguration(models.Model):
    ram = models.CharField(max_length=20)
    rom = models.CharField(max_length=20)

    class Meta:
        db_table = "phone_configuration"
        unique_together = ("ram", "rom")

    def __str__(self):
        return f"{self.ram}/{self.rom}"


class PhoneVariant(models.Model):
    phone = models.ForeignKey(Phone, on_delete=models.PROTECT)
    configuration = models.ForeignKey(PhoneConfiguration, on_delete=models.PROTECT)
    color = models.CharField(max_length=50)  # Màu sắc
    price = models.FloatField(null=False)  # Giá bán
    stock = models.IntegerField(default=0)  # Số lượng tồn kho
    sold_quantity = models.IntegerField(default=0)  # Số lượng đã bán
    img = models.ImageField(default='fallback.png', blank=False)

    class Meta:
        db_table = "phone_variant"
        unique_together = ("phone", "configuration", "color")  # UNIQUE trên cả phone

    def __str__(self):
        return f"{self.phone} - {self.color} - {self.configuration} - {self.price}$"