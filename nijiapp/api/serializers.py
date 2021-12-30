# from nijiapp.models import Properties
from django.contrib.auth import models
from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from rest_framework import serializers, validators
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import RefreshToken

from nijiapp.models import(
    Contact,
    # User,
    Map,
    # Categories,
    PropertyType,
    # SubCategories,
    Properties,
    Post,
    UserOTP,
    Watchlist,
    Images,
    BankDetail,
    NewsBlogs,
    ClientUser,
    Card,
    About,

)


# django dyanamic serializers for users and groups.

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
                queryset=User.objects.all(),
                fields=['username', ]
            )
        ]

    def create(self, validated_data):
        username, email, first_name, last_name, password, position = validated_data.values()

        instance = self.Meta.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        if password is not None:
            instance.set_password(password)
            instance.is_superuser = False
            instance.is_staff = False
            instance.save()
            if position:
                if position == 'users':
                    my_group = Group.objects.get(name='users') 
                    my_group.user_set.add(instance)
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
            'user': {'write_only': True}
        }


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=False)
    contact = serializers.SerializerMethodField(read_only=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'contact', 'token']

    def get_token(self, obj):
        token = str(RefreshToken.for_user(obj).access_token)
        user_qs = UserOTP.objects.filter(user=obj)
        if user_qs.exists():
            user_obj = user_qs.first()
            if user_obj.user_verified:
                return str(token)
            else:
                raise serializers.ValidationError("The user is not verified")
        else:
            raise serializers.DjangoValidationError("The user not exist")

    def get_contact(self, obj):
        try:
            return ContactSerializer(obj.usercontact, many=False).data
        except:
            return None


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        # fields = '__all__'
        fields = ['image_url']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PropertyTypeSerializer(serializers.ModelSerializer):

    # foreign_key_field = PropertiesSerializer()
    class Meta:
        model = PropertyType
        # fields = ['id', 'foreign_key_field', 'type']
        fields = ('property_type',)


class PropertiesSerializer(serializers.ModelSerializer):
    # images =serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username')
    # images = ImagesSerializer(source='images_set', many=True, read_only=True)
    images = serializers.SerializerMethodField()
    # post = PostSerializer(source='post', many=)

    class Meta:
        model = Properties
        fields = [
            'id',
            'title',
            'city',
            'district',
            'province',
            'price',
            'amenities',
            'landmarks',
            'map',
            'property',
            'user',
            'user_email',
            'thumbnail',
            'descriptions',
            'bedrooms',
            'bathroom',
            'parking',
            'kitchen',
            'floors',
            'builtup_area',
            'road_access',
            'property_type',
            'images',
            
        ]

        def create(self, validated_data):
            images_data = self.context.get('view').request.FILES
            property = Properties.objects.create(title=validated_data.get('title', 'no-title'), user_id=1)
            for image_data in images_data.values():
                Images.objects.create(property=property, image=image_data)
            return property

    def get_images(self, property):
        images_qs = Properties.images(property)
        # thumb = Properties.objects.first()
        if images_qs.exists():
            from django.contrib.sites.models import Site
            from django.conf import settings

            current_site = Site.objects.get_current()
            # images = [image.image_url.url for image in images_qs]
            full_images = [
                'http://%s%s%s' % (current_site.domain, settings.MEDIA_URL, image.image_url) for image in images_qs
            ]
            return full_images
        return []


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
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])
        # print(validated_data['position'])
        return user

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = '__all__'