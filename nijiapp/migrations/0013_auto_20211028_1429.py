# Generated by Django 3.2 on 2021-10-28 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nijiapp', '0012_auto_20211028_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='properties',
            name='property',
            field=models.CharField(choices=[('Buy', 'buy'), ('Rent', 'rent')], max_length=100),
        ),
        migrations.AlterField(
            model_name='userotp',
            name='counter',
            field=models.BigIntegerField(default=1),
        ),
    ]