# Generated by Django 3.2 on 2021-11-20 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nijiapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='properties',
            name='property',
            field=models.CharField(choices=[('Buy', 'buy'), ('Rent', 'rent')], max_length=100),
        ),
    ]