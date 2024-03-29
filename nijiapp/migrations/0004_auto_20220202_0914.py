# Generated by Django 2.2.20 on 2022-02-02 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nijiapp', '0003_auto_20220112_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='properties',
            name='land_area',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='position',
            field=models.CharField(choices=[('CEO', 'ceo'), ('Manager', 'manager')], max_length=100),
        ),
        migrations.AlterField(
            model_name='contact',
            name='visibility',
            field=models.CharField(choices=[('True', 'Yes'), ('False', 'No')], max_length=20),
        ),
        migrations.AlterField(
            model_name='properties',
            name='floors',
            field=models.DecimalField(decimal_places=10, max_digits=10),
        ),
        migrations.AlterField(
            model_name='properties',
            name='province',
            field=models.CharField(choices=[('Gandaki Province', 'gandaki province'), ('Karnali Province', 'karnali province'), ('Sudurpashchim Province', 'sudurpashchim province'), ('Province No. 2', 'province no 2'), ('Bagmati Province', 'bagmati province'), ('Lumbini Province', 'lumbini province'), ('Province No. 1', 'province no 1')], max_length=200),
        ),
    ]
