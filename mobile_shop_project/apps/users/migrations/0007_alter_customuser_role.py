# Generated by Django 5.1.6 on 2025-03-27 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('client', 'Client'), ('staff', 'Staff'), ('shopowner', 'ShopOwner'), ('admin', 'Admin')], default='client', max_length=10),
        ),
    ]
