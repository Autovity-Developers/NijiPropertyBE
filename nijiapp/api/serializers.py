# from nijiapp.models import Properties
from django.contrib.auth import models
from django.contrib.auth.models import Group, User
from django.db.models.query import QuerySet
from rest_framework import serializers, validators
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import RefreshToken

from nijiapp.models import(
    Contact,
    # User,
    Map,
    Categories,
    SubCategories,
    Properties,
    Post,
    Watchlist,
    Images,
    BankDetail,
    NewsBlogs,
    ClientUser,
  
) 


#django dyanamic serializers for users and groups.

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',) 


 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'password': {'write_only': True}
        }
        validators = [
            UniqueTogetherValidator(
                queryset = User.objects.all(),
                fields=['username',]
            )
        ]
    def create(self, validated_data):
        username, email, first_name, last_name, password = validated_data.values()

        instance = self.Meta.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        if password is not None:
            instance.set_password(password)
            instance.is_superuser=False
            instance.is_staff = False
            instance.save()
            return instance

    def update(self, instance, validated_data):
        for(key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'address', 'phone_no', 'visibility')
        # exclude = ('id', 'user')
        extra_kwargs = {
            'id': {'write_only': True},
            'user':{'write_only':True}
        }

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=False)
    contact = serializers.SerializerMethodField(read_only=False)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'contact', 'token']

    def get_token(self, obj):
        token = str(RefreshToken.for_user(obj).access_token)
        return str(token)
    
    def get_contact(self, obj):
        try:
            return ContactSerializer(obj.usercontact, many=False).data
        except:
            return None

class PropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Properties
        fields = '__all__'

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class SubCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategories
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'



class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = '__all__'

class BankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetail
        fields = '__all__'
        
class NewsBlogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsBlogs
        fields = '__all__'

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'

class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = '__all__'


# Normal User Serializer

class ClientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user


#try 

# class OTPCodeSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
    
#     def validate_email(self, email):
#         if User.objects.filter(email=email).count():
#             raise serializers.ValidationError('This email has been registered')
#         if not re.match(EMAIL_REGAX, email):
#             raise serializers.ValidationError('Mailbox format error')
#         one_minute_age = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
#         if OTPCode.objects.filter(add_time__gt=one_minute_age, email=email).count():
#             raise serializers.ValidationError('Please send again in a minute')
#         return email

