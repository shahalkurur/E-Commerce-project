# Generated by Django 4.2.6 on 2024-01-21 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0014_alter_coupen_discount_alter_coupen_mini_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='amount',
            field=models.FloatField(default=0.0),
        ),
    ]
