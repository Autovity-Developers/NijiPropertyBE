# Generated by Django 2.2.20 on 2022-01-11 08:57

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(upload_to='Image_Gallery/about_company')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BankDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=100)),
                ('interest_rate', models.DecimalField(decimal_places=50, max_digits=100)),
                ('process_charge', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(upload_to='Image_Gallery/card')),
                ('position', models.CharField(choices=[('CEO', 'ceo'), ('Manager', 'manager')], max_length=100)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClientUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(blank=True, max_length=100, null=True)),
                ('position', models.CharField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewsBlogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('post', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Properties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=200, null=True)),
                ('city', models.CharField(max_length=200, null=True)),
                ('district', models.CharField(max_length=200, null=True)),
                ('province', models.CharField(choices=[('Province No. 2', 'province no 2'), ('Karnali Province', 'karnali province'), ('Sudurpashchim Province', 'sudurpashchim province'), ('Gandaki Province', 'gandaki province'), ('Bagmati Province', 'bagmati province'), ('Lumbini Province', 'lumbini province'), ('Province No. 1', 'province no 1')], max_length=200)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('amenities', models.CharField(blank=True, max_length=200, null=True)),
                ('landmarks', models.CharField(blank=True, max_length=200, null=True)),
                ('property', models.CharField(choices=[('Buy', 'buy'), ('Rent', 'rent')], max_length=100)),
                ('user_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('user_contact', models.CharField(blank=True, max_length=100, null=True)),
                ('thumbnail', models.ImageField(upload_to='Image_Gallery/thumbnail')),
                ('descriptions', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('bedrooms', models.IntegerField(blank=True, null=True)),
                ('bathroom', models.IntegerField(blank=True, null=True)),
                ('parking', models.CharField(blank=True, max_length=100, null=True)),
                ('kitchen', models.IntegerField(blank=True, null=True)),
                ('floors', models.IntegerField(blank=True, null=True)),
                ('builtup_area', models.CharField(blank=True, max_length=100, null=True)),
                ('road_access', models.CharField(blank=True, max_length=100, null=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('is_premium', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nijiapp.Properties')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserOTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_verified', models.BooleanField(default=False)),
                ('counter', models.BigIntegerField(default=1)),
                ('otp_code', models.CharField(blank=True, max_length=6, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon_name', models.CharField(blank=True, max_length=100, null=True)),
                ('property_type', models.CharField(blank=True, max_length=100, null=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ptype', to='nijiapp.Properties')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('url', models.URLField()),
                ('icon', models.CharField(blank=True, max_length=200, null=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nijiapp.Properties')),
            ],
        ),
        migrations.CreateModel(
            name='OTPCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=8, verbose_name=' Verification Code ')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name=' Generation time ')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.DecimalField(decimal_places=50, max_digits=100)),
                ('latitude', models.DecimalField(decimal_places=50, max_digits=100)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maps', to='nijiapp.Properties')),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.ImageField(upload_to='Image_Gallery')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nijiapp.Properties')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=500)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=500)),
                ('phone_no', models.IntegerField(blank=True, null=True)),
                ('visibility', models.CharField(choices=[('False', 'No'), ('True', 'Yes')], max_length=20)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usercontact', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
