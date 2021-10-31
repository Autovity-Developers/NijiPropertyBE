from django.db import models
from django.contrib.auth.models import Group, User

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

class Map(models.Model):
    property_title = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.DecimalField(max_digits=100, decimal_places=50)
    latitude = models.DecimalField(max_digits=100, decimal_places=50)

    def __str__(self):
        return self.property_title

class Categories(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title

class SubCategories(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

property_choices = {
    ('Buy', 'buy'),
    ('Rent', 'rent')
}
class Properties(models.Model):
    title = models.CharField(max_length=200, default='', null=True)
    address = models.CharField(max_length=200, null=True)
    price = models.IntegerField(blank=True, null=True)
    facilities = models.CharField(max_length=200, blank=True, null=True)
    amenities = models.CharField(max_length=200, null=True, blank=True)
    landmarks = models.CharField(max_length=200, null=True, blank=True)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    # post = models.ForeignKey(Post, on_delete=models.CASCADE)
    property = models.CharField(max_length=100, choices=property_choices)    
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategories, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


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
        return str(self.property)

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

    def __str__(self):
        return self.username

class UserOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None)
    user_verified = models.BooleanField(default=False)
    counter = models.BigIntegerField(default=1)
    otp_code = models.CharField(max_length=6, null=True,blank=True)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)


    def __str__(self):
        return self.user.username



