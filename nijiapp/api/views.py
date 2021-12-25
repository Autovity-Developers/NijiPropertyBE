import re
from django.db.models import query
from rest_framework import status
from django.db.models.base import ModelStateFieldsCacheDescriptor
from django.db.models.manager import BaseManager
import rest_framework
from django.http import Http404
from django.contrib.auth.models import Group, User
from nijiapp.models import (BankDetail, Contact, Images, Map,
                            NewsBlogs, Post, Properties, PropertyType, UserOTP,
                            Watchlist, OTPCode, Card, About)
from rest_framework import (authentication, permissions, serializers, status,
                            viewsets, generics)
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.paginator import Paginator
from django.core.mail import send_mail

from .serializers import (ContactSerializer, GroupSerializer, PostSerializer, PropertiesSerializer,
                           PropertyTypeSerializer, UserSerializer, UserSerializerWithToken, MapSerializer, 
                           BankDetailSerializer, NewsBlogsSerializer, ImagesSerializer, WatchListSerializer,
                           ClientUserSerializer, RegisterClientSerializer, CardSerializer, AboutSerializer)

from nijiapp.otp_helper import send_otp,verify_otp
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
# from django_filters.rest_framework import DjangoFilterBackend

@api_view(['GET'])
# @permission_classes((AllowAny, ))
def api_list(request):
    objs = {
        'login': '/api/api_list/login',
        'properties': '/api/api_list/properties',
        'properties_detail_update_retrive': '/api/api_list/properties/<str:title>/',
        # 'property_type': '/api/api_list/property_type',
        # 'property_type_detail_update_retrive': '/api/api_list/property_type/<str:title>/',
        # 'prop_subcategory': '/api/api_list/prop_subcategory',
        # 'prop_subcategory_detail_update_retrive': '/api/api_list/prop_subcategory/<int:pk>/',
        'post':'/api/api_list/post',
        'post_detail_update_retrive': '/api/api_list/post/<int:pk>/',
        'contact':'/api/api_list/contact',
        'contact_detail_update_retrive': '/api/api_list/contact/<int:pk>/',
        'map':'/api/api_list/map',
        'map_detail_update_retrive': '/api/api_list/map/<int:pk>/',
        'bank':'/api/api_list/bank',
        'bank_detail_update_retrive': '/api/api_list/bank/<int:pk>/',
        # 'images':'/api/api_list/images',
        # 'images_detail_update_retrive': '/api/api_list/images/<int:pk>/',
        'wathlist':'/api/api_list/watchlist',
        'watchlist_detail_update_retrive': '/api/api_list/watchlist/<int:pk>/',
        'featured_properties': '/api/api_list/featured/',
        'premium_properties': '/api/api_list/premuim/',
        # 'register': '/api/api_list/register/',
        # 'otp': '/api/api_list/otp/',
        
        

    }
    return Response(objs)



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


def check_agent_group(request):
    if request.user.groups.filter(name='agent').exists():
        return True
    return False

def check_editor_group(request):
    if request.user.groups.filter(name='editor').exists():
        return True
    return False

def check_user_group(request):
    if request.user.groups.filter(name='users').exists():
        return True
    return False

def check_mod_group(request):
    if request.user.groups.filter(name='mod').exists():
        return True
    return False

class PropertyList(ListAPIView):
    queryset = Properties.objects.all().order_by('id')
    pagination_class = PageNumberPagination
    pagination_class.page_size = 6

    serializer_class = PropertiesSerializer

    # def get(self, request):
    #     properties = Properties.objects.all().order_by('id')
    #     serializer = PropertiesSerializer(properties, context={'request':request})
    #     return Response(serializer.data)
   

class PropertyCreateView(APIView):
    def post(self, request, format=None):
        if check_agent_group(request) or check_editor_group(request): 
            req = request.POST 
            if req.get('title'):    
                if Properties.objects.filter(title__iexact=req.get('title')).exists():
                    return Response({'error':True, 'message':'A property with same name already exists'}, status=status.HTTP_400_BAD_REQUEST)
                map = Map.objects.get(pk=req.get('map'))
                
                property_type = PropertyType.objects.get(pk=req.get('property_type'))
                # subcategory = SubCategories.objects.get(pk=req.get('subcategory'))
                property = Properties(
                    title = req.get('title'),
                    # address = req.get('address'),
                    city = req.get('city'),
                    district = req.get('district'),
                    province = req.get('province'),
                    price = req.get('price'),
                    # facilities = req.get('facilities'),
                    amenities = req.get('amenities'),
                    landmarks = req.get('landmarks'),
                    map = map,
                    property = req.get('property'),
                    property_type = property_type,
                    user = request.user,
                    thumbnail = req.get('thumbnail'),
                    descriptions = req.get('descriptions'),
                    bedrooms = req.get('bedrooms'),
                    bathroom = req.get('bathroom'),
                    parking = req.get('parking'),
                    kitchen = req.get('kitchen'),
                    floors = req.get('floors'),
                    builtup_area = req.get('builtup_area'),
                    road_access = req.get('road_access'),

                )
                property.save()
                serializer = PropertiesSerializer(property, many=False)
                return Response(serializer.data)
            else:
                return Response({'error':True,'message':'Please supply all required details'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class PropertyDetailView(APIView):
    """
    Retrieve, update or delete a property instance.
    """
    # permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.IsAdminUser]

    
    def get_object(self, title):
        try:
            return Properties.objects.get(title=title)
        except Properties.DoesNotExist:
            raise Http404
    
    def get(self, request, title, format=None):
        property = self.get_object(title)
        serializer = PropertiesSerializer(property)
        return Response(serializer.data)

    def put(self, request, title, format=None):
        if check_agent_group(request) or check_editor_group(request):
            property = self.get_object(title)
            serializer = PropertiesSerializer(property, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def delete(self, request, title, format=None):
        if check_agent_group(request) or check_editor_group(request):
            property = self.get_object(title)
            property.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class PropertyTypeListCreateView(APIView):

    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        prop_type = PropertyType.objects.all()
        serializer = PropertyTypeSerializer(prop_type, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        if check_agent_group(request) or check_editor_group(request):   
            serializer =  PropertyTypeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class PropertyTypeDetailView(APIView):

    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, type):
        try:
            return PropertyType.objects.get(property_type=type)
        except PropertyType.DoesNotExist:
            raise Http404
    
    def get(self, request, type, format=None):
        prop_type = self.get_object(type)
        serializer = PropertyTypeSerializer(prop_type)
        return Response(serializer.data)
    
    def put(self, request, type, format=None):
        if check_agent_group(request) or check_editor_group(request):
            prop_type = self.get_object(type)
            serializer = PropertyTypeSerializer(prop_type, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def delete(self, request, type, format=None):
        if check_agent_group(request) or check_editor_group(request):
            prop_type = self.get_object(type)
            prop_type.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class SearchView(APIView):
    def get(self, request):
        qs = Properties.objects.all()
        price = request.GET.get('price')
        if price:
            qs = qs.filter(price__icontains=price)
        print(self.kwargs)

        property =request.GET.get('property')
        if property:
            qs = qs.filter(property__icontains=property)

        city = request.GET.get('city')
        if city:
            qs = qs.filter(city__icontains=city)

        district = request.GET.get('district')
        if district:
            qs = qs.filter(district__icontains=district)
        
        province = request.GET.get('province')
        if province:
            qs = qs.fiter(province__icontains=province)
            
        property_type = request.GET.get('property_type')
        print(property_type)
        if property_type:
            qs = qs.filter(property_type__title=property_type)
        queryset = qs
        # return queryset
        serializer =PropertiesSerializer(qs, many=True)
        return Response(serializer.data)

class PostListCreateView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

    
    def post(self, request, format=None):
        if check_agent_group(request) or check_editor_group(request):
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class PostDetailView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        if check_agent_group(request) or check_editor_group(request):
            post = self.get_object(pk)
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def delete(self, request, pk, format=None):
        if check_editor_group(request) or check_agent_group(request):
            post = self.get_object(pk)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ContactListCreateView(APIView):
   
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        contact = Contact.objects.all()
        serializer = ContactSerializer(contact, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if check_agent_group(request) or check_editor_group(request):
            serializer = ContactSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class ContactDetailView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        contact = self.get_object(pk)
        serializer = ContactSerializer(contact)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        if check_agent_group(request) or check_editor_group(request):    
            contact = self.get_object(pk)
            serializer = ContactSerializer(contact, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def delete(self, request, pk, format=None):
        if check_editor_group(request) or check_agent_group(request):
            contact = self.get_object(pk)
            contact.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class MapListCreateView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        map = Map.objects.all()
        serializer = MapSerializer(map, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if check_agent_group(request) or check_editor_group(request):    
            serializer = MapSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class MapDetailView(APIView):

    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Map.objects.get(pk=pk)
        except Map.DoesNotExist:
            raise Http404 
   
    def get(self, request, pk, format=None):
        map = self.get_object(pk)
        serializer = MapSerializer(map)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if check_editor_group(request) or check_agent_group(request):
            map = self.get_object(pk)
            serializer = MapSerializer(map, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, pk, format=None):
        if check_agent_group(request) or check_editor_group(request):
            map = self.get_object(pk)
            map.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class BankListCreateView(APIView):

    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        bank = BankDetail.objects.all()
        serializer = BankDetailSerializer(bank, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if check_editor_group(request):
            serializer = BankDetailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class BankDetailView(APIView):

    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return BankDetail.objects.get(pk=pk)
        except BankDetail.DoesNotExist:
            raise Http404 


    def get(self, request, pk, format=None):
        bank = self.get_object(pk)
        serializer = BankDetailSerializer(bank)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if check_editor_group(request):
            bank = self.get_object(pk)
            serializer = BankDetailSerializer(bank, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, pk, format=None):
        if check_editor_group(request):
            bank = self.get_object(pk)
            bank.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class NewsBlogsListCreateView(APIView):

    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        newsblog = NewsBlogs.objects.all()
        serializer = NewsBlogsSerializer(newsblog, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if check_editor_group(request) or check_agent_group(request):
            serializer = NewsBlogsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class NewsBlogsDetailView(APIView):

    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return NewsBlogs.objects.get(pk=pk)
        except NewsBlogs.DoesNotExist:
            raise Http404 


    def get(self, request, pk, format=None):
        newsblog = self.get_object(pk)
        serializer = NewsBlogsSerializer(newsblog)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if check_agent_group(request) or check_editor_group(request):
            newsblog = self.get_object(pk)
            serializer = NewsBlogsSerializer(newsblog, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, pk, format=None):
        if check_editor_group(request) or check_agent_group(request):
            newsblog = self.get_object(pk)
            newsblog.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ImagesListCreateView(APIView):

    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        image = Images.objects.all()
        serializer = ImagesSerializer(image, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if check_agent_group(request) or check_editor_group(request):
            serializer = ImagesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class ImagesDetailView(APIView):

    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Images.objects.get(pk=pk)
        except Images.DoesNotExist:
            raise Http404 


    def get(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImagesSerializer(image, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if check_editor_group(request) or check_agent_group(request):
            image = self.get_object(pk)
            serializer = ImagesSerializer(image, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, pk, format=None):
        if check_agent_group(request) or check_editor_group(request):
            image = self.get_object(pk)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class WatchListCreateView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        if check_user_group(request):
            watchlist = Watchlist.objects.filter(user=request.user)
            serializer = WatchListSerializer(watchlist, many=True)
            return Response(serializer.data)
        else:
            return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


    def post(self, request, format=None):
        if check_user_group(request):
            serializer = WatchListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class WatchlistDetailView(APIView):

    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Watchlist.objects.get(pk=pk)
        except Watchlist.DoesNotExist:
            raise Http404 


    def get(self, request, pk, format=None):
        watchlist = self.get_object(pk)
        serializer = WatchListSerializer(watchlist)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        # if check_editor_group(request):
            watchlist = self.get_object(pk)
            serializer = WatchListSerializer(watchlist, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #    return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, pk, format=None):
        if check_user_group(request):
            watchlist = self.get_object(pk)
            watchlist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterClientSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        res = send_otp(user,user.email)
        print(res)
        return Response({
        "user": ClientUserSerializer(user, context=self.get_serializer_context()).data,
        })


class VerifyOTPView(APIView):
    def post(self, request):
        try:
            otp_code = request.POST.get('otp_code')
            email = request.POST.get('email')
            user = User.objects.get(email=request.POST.get('email'))
            res = False
            if user:
                res = verify_otp(user, user.email, str(otp_code))
            
            if res:
                user_otp_obj = UserOTP.objects.get(user=user)
                user_otp_obj.user_verified = True
                user_otp_obj.otp_code = None
                user_otp_obj.save()
                return Response(data = {"message":"success"}, status=status.HTTP_200_OK)
            else:
                return Response(data = {'message':'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            # results = Properties.objects.filter(property_type = 'holding', location = 'kathmandu', '', )
            # serialiazer = PeropertySerialiazer(results, many=True)
        except Exception as e:
            print(e)
            return Response(data={"message":"server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# from rest_framework.response import Response
# from rest_framework.views import status
# from rest_framework import mixins, viewsets
from random import randint

def generate_otp(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

class SendOTPView(APIView):
    def get(self, request):
        code = generate_otp(6)
        try:
            otp_obj = OTPCode.objects.create(user=request.user, code=code)
            otp_obj.save()
        except:
            otp_obj = OTPCode.objects.get(user=request.user)
            otp_obj.code = code
            otp_obj.save()
        

        try:
            #send code via mail
            user=request.user
            email = user.email
            send_mail(
             'OTP code',
             otp_obj,
              'insurance.chaiyo.info@gmail.com',
                [email],
              fail_silently=False,
)

            #if mail succcessfully sent?
            return Response(data={'message':'Mail sent'},status=status.HTTP_200_OK)

        except:
            return Response(data={'message':'Unable to send mail'}, status=status.HTTP_400_BAD_REQUEST)
    
    # serializer_class = UserSerializer

    def post(self, request):
        user = request.user
        otp_obj = OTPCode.objects.get(user=user)
        user_submitted_otp = request.POST.get('otp_code') 
        if otp_obj.code == user_submitted_otp:
            return Response(data={'message':'User verified'}, status=status.HTTP_200_OK)
        return Response(data={'message':'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

class FeatureProperties(APIView):
    
    def get(self, request, fromat=None):
        feature = Properties.objects.filter(is_featured=True)[:4] 
        serializer = PropertiesSerializer(feature, many=True)
        return Response(serializer.data)

class PremiumProperties(APIView):

    def get(self, request, format=None):
        premium = Properties.objects.filter(is_premium=True)
        serializer = PropertiesSerializer(premium, many=True)
        return Response(serializer.data)



class CardListCreateView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        card = Card.objects.all()
        serializer = CardSerializer(card, many=True)
        return Response(serializer.data)

    
    def post(self, request, format=None):
        if check_agent_group(request) or check_editor_group(request):
            serializer = CardSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CardDetailView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Card.objects.get(pk=pk)
        except Card.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        card = self.get_object(pk)
        serializer = PostSerializer(card)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        if check_agent_group(request) or check_editor_group(request):
            card = self.get_object(pk)
            serializer = PostSerializer(card, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def delete(self, request, pk, format=None):
        if check_editor_group(request) or check_agent_group(request):
            card = self.get_object(pk)
            card.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


class AboutListCreateView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        about = About.objects.all()
        serializer = CardSerializer(about, many=True)
        return Response(serializer.data)

    
    def post(self, request, format=None):
        if check_agent_group(request) or check_editor_group(request):
            serializer = AboutSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class AboutDetailView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return About.objects.get(pk=pk)
        except About.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        about = self.get_object(pk)
        serializer = AboutSerializer(about)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        if check_agent_group(request) or check_editor_group(request):
            about = self.get_object(pk)
            serializer = AboutSerializer(about, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def delete(self, request, pk, format=None):
        if check_editor_group(request) or check_agent_group(request):
            about = self.get_object(pk)
            about.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)