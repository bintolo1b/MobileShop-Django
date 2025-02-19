# Generated by Django 5.1.6 on 2025-02-19 13:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.OneToOneField(default=-1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, to_field='username'),
            preserve_default=False,
        ),
    ]
