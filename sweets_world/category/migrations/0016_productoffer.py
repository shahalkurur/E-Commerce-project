# Generated by Django 4.2.6 on 2024-01-23 02:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0015_alter_wallet_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_type', models.CharField(choices=[('percentage', 'Percentage'), ('fixed', 'Fixed')], default='fixed', max_length=10)),
                ('discount_value', models.IntegerField()),
                ('start_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('expire_date', models.DateTimeField(blank=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
        ),
    ]
