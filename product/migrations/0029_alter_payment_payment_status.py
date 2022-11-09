# Generated by Django 4.1.2 on 2022-11-09 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0028_alter_payment_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('SUCCESS', 'sucess'), ('FAILED', 'failed')], default='PENDING', max_length=100),
        ),
    ]
