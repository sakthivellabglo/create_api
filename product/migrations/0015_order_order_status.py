# Generated by Django 4.1.2 on 2022-10-26 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_alter_order_tax_alter_order_total_product_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('pending', 'pending'), ('sucess', 'sucess'), ('failed', 'failed')], default='pending', max_length=15),
        ),
    ]
