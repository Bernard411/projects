# Generated by Django 3.2.13 on 2024-05-29 21:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20240529_0639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='price',
        ),
    ]
