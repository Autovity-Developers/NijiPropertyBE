# Generated by Django 3.2.6 on 2021-10-24 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nijiapp', '0008_auto_20211008_1803'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTPCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(blank=True, max_length=11, verbose_name=' cell-phone number ')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email')),
                ('code', models.CharField(max_length=8, verbose_name=' Verification Code ')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name=' Generation time ')),
            ],
        ),
        migrations.AlterField(
            model_name='contact',
            name='visibility',
            field=models.CharField(choices=[('True', 'Yes'), ('False', 'No')], max_length=20),
        ),
    ]