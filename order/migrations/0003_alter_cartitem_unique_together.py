# Generated by Django 5.1.5 on 2025-03-10 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_cart_id'),
        ('product', '0002_alter_product_options_review'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('cart', 'product')},
        ),
    ]
