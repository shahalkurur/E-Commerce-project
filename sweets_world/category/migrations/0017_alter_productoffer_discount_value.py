# Generated by Django 4.2.6 on 2024-01-23 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0016_productoffer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoffer',
            name='discount_value',
            field=models.IntegerField(blank=True),
        ),
    ]
