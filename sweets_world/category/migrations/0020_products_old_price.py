# Generated by Django 4.2.6 on 2024-01-23 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0019_products_has_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='old_price',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
