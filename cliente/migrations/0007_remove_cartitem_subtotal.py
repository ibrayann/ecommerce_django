# Generated by Django 4.2.2 on 2023-06-30 01:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0006_cartitem_subtotal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='subtotal',
        ),
    ]
