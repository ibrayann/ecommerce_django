# Generated by Django 4.2.2 on 2023-07-07 05:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0012_product_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.product')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.purchase')),
            ],
        ),
    ]
