from django.contrib import admin
from .models import(

    Contact,
    Map,
    Properties,
    PropertyType,
    Post,
    UserOTP,
    Watchlist,
    Images,
    BankDetail,
    NewsBlogs,
    ClientUser,
    OTPCode,
    Card,
    About,

) 
# Register your models here.

admin.site.register(Contact)

admin.site.register(Map)
# admin.site.register(Categories)
# admin.site.register(SubCategories)
admin.site.register(Properties)
admin.site.register(PropertyType)
admin.site.register(Post)
admin.site.register(BankDetail)
# admin.site.register(NewsBlogs) puased
admin.site.register(ClientUser)
admin.site.register(UserOTP)
admin.site.register(OTPCode)
admin.site.register([Watchlist, Images, Card, About])