# Generated by Django 4.1.7 on 2023-03-06 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_cart_cartitem_cart_items_cart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='available_plates',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
