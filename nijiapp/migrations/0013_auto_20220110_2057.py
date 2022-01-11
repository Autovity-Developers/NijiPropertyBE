# Generated by Django 2.2.20 on 2022-01-10 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nijiapp', '0012_auto_20220110_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertytype',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='card',
            name='position',
            field=models.CharField(choices=[('CEO', 'ceo'), ('Manager', 'manager')], max_length=100),
        ),
        migrations.AlterField(
            model_name='properties',
            name='province',
            field=models.CharField(choices=[('Sudurpashchim Province', 'sudurpashchim province'), ('Gandaki Province', 'gandaki province'), ('Karnali Province', 'karnali province'), ('Lumbini Province', 'lumbini province'), ('Province No. 1', 'province no 1'), ('Bagmati Province', 'bagmati province'), ('Province No. 2', 'province no 2')], max_length=200),
        ),
        migrations.AlterField(
            model_name='propertytype',
            name='property_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
