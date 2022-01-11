from django.db import models
from django.contrib.auth.models import Group, User
import datetime
from ckeditor_uploader.fields import  RichTextUploadingField
# from ckeditor.fields import RichTextField, RichTextUploadingField
from django.db.models.aggregates import Max 
# now = str(datetime.datetime)

# Create your models here.
# class UserType(models.Model):
#     type = models.CharField(max_length=500, unique=True)
#     policies = models.CharField(max_length=500)

#     def __str__(self):
#         return self.type

# contact is also useless if the users are not access as custom
my_choices = {
    ('True', 'Yes'),
    ('False', 'No')
}

class Contact(models.Model):
    name = models.CharField(max_length=500, default='')
    email = models.EmailField()
    address = models.CharField(max_length=500)
    phone_no = models.IntegerField(blank=True, null=True)
    visibility = models.CharField(max_length=20, choices=my_choices)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='usercontact')

    def __str__(self):
        return self.name

# class User(models.Model):
#     username = models.CharField(max_length=500, default='')
#     password = models.CharField(max_length=500)
#     type = models.ForeignKey(UserType, on_delete=models.CASCADE)
#     contact_details = models.ForeignKey(Contact, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.username



# class Categories(models.Model):
#     title = models.CharField(max_length=200, blank=True, null=True)

#     def __str__(self):
#         return self.title

# class SubCategories(models.Model):
#     title = models.CharField(max_length=200, blank=True, null=True)
#     category = models.ForeignKey(Categories, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.title

class PropertyType(models.Model):
    icon_name = models.CharField(max_length=100, null=True, blank=True)
    property_type = models.CharField(max_length=100, null=True, blank=True)
    # property = models.ForeignKey(Properties, on_delete=models.CASCADE, related_name='ptype')
    
    # def __str__(self):
    #     return self.property.title

    def __str__(self):
        return str(self.property_type)
    
    def __repr__(self):
        return self.property_type


property_choices = {
    ('Buy', 'buy'),
    ('Rent', 'rent')
}
province = {
    ('Province No. 1', 'province no 1'),
    ('Province No. 2', 'province no 2'),
    ('Bagmati Province', 'bagmati province'),
    ('Gandaki Province', 'gandaki province'),
    ('Lumbini Province', 'lumbini province'),
    ('Karnali Province', 'karnali province'),
    ('Sudurpashchim Province', 'sudurpashchim province'),
}
class Properties(models.Model):
    title = models.CharField(max_length=200, default='', null=True)
    # address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    district = models.CharField(max_length=200, null=True)
    province = models.CharField(max_length=200, choices=province)
    price = models.IntegerField(blank=True, null=True)
    # facilities = models.CharField(max_length=200, blank=True, null=True)#remove
    amenities = models.CharField(max_length=200, null=True, blank=True)
    landmarks = models.CharField(max_length=200, null=True, blank=True)
    # map = models.ForeignKey(Map, on_delete=models.CASCADE)
    property = models.CharField(max_length=100, choices=property_choices) 
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)   
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_email = models.EmailField(blank=True, null=True)
    user_contact = models.CharField(max_length=100, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='Image_Gallery/thumbnail')
    descriptions = RichTextUploadingField(blank=True, null=True)
    bedrooms = models.IntegerField(blank=True, null=True)
    bathroom = models.IntegerField(blank=True, null=True)
    parking = models.CharField(max_length=100, null=True, blank=True)
    kitchen = models.IntegerField(blank=True, null=True)
    floors = models.IntegerField(blank=True, null=True)
    builtup_area = models.CharField(max_length=100, null=True, blank=True)
    road_access = models.CharField(max_length=100, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    # def get_images(self, obj):
    #     return obj.image_url_set.first().image.url

    @classmethod
    def images(cls, object=None):
        if object:
            return Images.objects.filter(property=object)
    
    @classmethod
    def maps(cls, object=None):
        if object:
            return Map.objects.filter(property=object)

     
    # @classmethod
    # def proptypes(cls, object=None):
    #     if object:
    #         return PropertyType.objects.filter(property=object)

    # @property
    # def get_status(self):
    #     if len(self.maps.all())> 0:
    #         return True
    #     else:
    #         return False
    

    def __str__(self):
        return self.title

    

class Map(models.Model):
    # property_title = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.DecimalField(max_digits=100, decimal_places=50)
    latitude = models.DecimalField(max_digits=100, decimal_places=50)
    property = models.ForeignKey(Properties, on_delete=models.CASCADE, related_name='maps')

    def __str__(self):
        return self.property.title


class Post(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField()
    icon = models.CharField(max_length=200, null=True, blank=True)
    property =models.ForeignKey(Properties, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Watchlist(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.property)

class Images(models.Model):
    image_url = models.ImageField(upload_to='Image_Gallery')
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)

    def __str__(self):
        return self.property.title

    def delete(self, *args, **kwargs):
        self.image_url.delete()
        super().delete(*args, **kwargs)

class BankDetail(models.Model):
    bank_name = models.CharField(max_length=100, null=False, blank=False)
    interest_rate = models.DecimalField(max_digits=100, decimal_places=50,null=False, blank=False)
    process_charge =models.IntegerField(null=False, blank=False)
    email = models.EmailField()
    url = models.URLField()

    def __str__(self):
        return self.bank_name

class NewsBlogs(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    post = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title

#for normal client user

class ClientUser(models.Model):
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.username

#try

class OTPCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=8, verbose_name=" Verification Code ")
    add_time = models.DateTimeField(verbose_name=' Generation time ', auto_now_add=True)


class UserOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None)
    user_verified = models.BooleanField(default=False)
    counter = models.BigIntegerField(default=1)
    otp_code = models.CharField(max_length=6, null=True,blank=True)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)


    def __str__(self):
        return self.user.username

position = {
    ('CEO', 'ceo'),
    ('Manager', 'manager')
}
class Card(models.Model):
    name = models.CharField(max_length=100, null=True,blank=True)
    image =models.ImageField(upload_to='Image_Gallery/card')
    position =models.CharField(max_length=100, choices=position)
    description = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
       return self.name

class About(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='Image_Gallery/about_company')
    description = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return self.title

        
# class SubscribeUser(models.Model):
#     username = models.CharField(max_length=100, null=True, blank=True)
#     email = models.EmailField()

#     def __str__(self):
#         return self.username

