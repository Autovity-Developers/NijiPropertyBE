import re
from rest_framework import status
from django.db.models.base import ModelStateFieldsCacheDescriptor
from django.db.models.manager import BaseManager
import rest_framework
from django.http import Http404
from django.contrib.auth.models import Group, User
from nijiapp.models import (BankDetail, Categories, Contact, Images, Map,
                            NewsBlogs, OTPCode, Post, Properties, SubCategories, UserOTP,
                            Watchlist)
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

from .serializers import (ContactSerializer, GroupSerializer, PostSerializer, PropertiesSerializer,  CategoriesSerializer,
                           SubCategoriesSerializer, UserSerializer, UserSerializerWithToken, MapSerializer, 
                           BankDetailSerializer, NewsBlogsSerializer, ImagesSerializer, WatchListSerializer,
                           ClientUserSerializer, RegisterClientSerializer, )

from nijiapp.otp_helper import send_otp,verify_otp

@api_view(['GET'])
def api_list(request):
    objs = {
        'login': '/api/api_list/login',
        'properties': '/api/api_list/properties',
        'properties_detail_update_retrive': '/api/api_list/properties/<int:pk>/',
        'prop_category': '/api/api_list/prop_category',
        'prop_category_detail_update_retrive': '/api/api_list/prop_category/<int:pk>/',
        'prop_subcategory': '/api/api_list/prop_subcategory',
        'prop_subcategory_detail_update_retrive': '/api/api_list/prop_subcategory/<int:pk>/',
        'post':'/api/api_list/post',
        'post_detail_update_retrive': '/api/api_list/post/<int:pk>/',
        'contact':'/api/api_list/contact',
        'contact_detail_update_retrive': '/api/api_list/contact/<int:pk>/',
        'map':'/api/api_list/map',
        'map_detail_update_retrive': '/api/api_list/map/<int:pk>/',
        'bank':'/api/api_list/bank',
        'bank_detail_update_retrive': '/api/api_list/bank/<int:pk>/',
        'images':'/api/api_list/images',
        'images_detail_update_retrive': '/api/api_list/images/<int:pk>/',
        'wathlist':'/api/api_list/watchlist',
        'watchlist_detail_update_retrive': '/api/api_list/watchlist/<int:pk>/',
        'register': '/api/api_list/register/',
        'otp': '/api/api_list/otp/',
        
        

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

def check_mod_group(request):
    if request.user.groups.filter(name='mod').exists():
        return True
    return False

class PropertyListCreateView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.IsAdminUser]


    def get(self, request, format=None):
        property_list = Properties.objects.all().order_by('id')
        page_number = self.request.query_params.get('page_number ', 1)
        page_size = self.request.query_params.get('page_size ', 6)
        paginator = Paginator(property_list , page_size)
        serializer = PropertiesSerializer(paginator.page(page_number) , many=True, context={'request':request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        if check_agent_group(request) or check_editor_group(request): 
            req = request.POST 
            if req.get('title'):    
                if Properties.objects.filter(title__iexact=req.get('title')).exists():
                    return Response({'error':True, 'message':'A property with same name already exists'}, status=status.HTTP_400_BAD_REQUEST)
                map = Map.objects.get(pk=req.get('map'))
                
                category = Categories.objects.get(pk=req.get('category'))
                subcategory = SubCategories.objects.get(pk=req.get('subcategory'))
                property = Properties(
                    title = req.get('title'),
                    address = req.get('address'),
                    price = req.get('price'),
                    facilities = req.get('facilities'),
                    amenities = req.get('amenities'),
                    landmarks = req.get('landmarks'),
                    map = map,
                    category = category,
                    subcategory= subcategory,
                    user = request.user,
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

    
    def get_object(self, pk):
        try:
            return Properties.objects.get(pk=pk)
        except Properties.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        property = self.get_object(pk)
        serializer = PropertiesSerializer(property)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if check_agent_group(request) or check_editor_group(request):
            property = self.get_object(pk)
            serializer = PropertiesSerializer(property, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def delete(self, request, pk, format=None):
        if check_agent_group(request) or check_editor_group(request):
            property = self.get_object(pk)
            property.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class CategoryListCreateView(APIView):

    def get(self, request, format=None):
        prop_cat = Categories.objects.all()
        serializer = CategoriesSerializer(prop_cat, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        if check_agent_group(request) or check_editor_group(request):   
            serializer =  CategoriesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoryDetailView(APIView):

    def get_object(self, pk):
        try:
            return Categories.objects.get(pk=pk)
        except Categories.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        prop_cat = self.get_object(pk)
        serializer = CategoriesSerializer(prop_cat)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        if check_agent_group(request) or check_editor_group(request):
            prop_cat = self.get_object(pk)
            serializer = CategoriesSerializer(prop_cat, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def delete(self, request, pk, format=None):
        if check_agent_group(request) or check_editor_group(request):
            prop_cat = self.get_object(pk)
            prop_cat.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class SubCategoryListCreateView(APIView):

    def get(self, request, format=None):
        prop_subcat =SubCategories.objects.all()
        serializer = SubCategoriesSerializer(prop_subcat, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        if check_agent_group(request) or check_editor_group(request):
            serializer =  SubCategoriesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SubCategoryDetailView(APIView):

    def get_object(self, pk):
        try:
            return SubCategories.objects.get(pk=pk)
        except SubCategories.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        prop_subcat = self.get_object(pk)
        serializer = SubCategoriesSerializer(prop_subcat)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        if check_agent_group(request) or check_editor_group(request):
            prop_subcat = self.get_object(pk)
            serializer = SubCategoriesSerializer(prop_subcat, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def delete(self, request, pk, format=None):
        if check_editor_group(request) or check_agent_group(request):
            prop_subcat = self.get_object(pk)
            prop_subcat.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



class PostListCreateView(APIView):

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

    def get_object(self, pk):
        try:
            return Images.objects.get(pk=pk)
        except Images.DoesNotExist:
            raise Http404 


    def get(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImagesSerializer(image)
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

    def get(self, request, format=None):
        watchlist = Watchlist.objects.all()
        serializer = WatchListSerializer(watchlist, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if check_editor_group(request):
            serializer = WatchListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class WatchlistDetailView(APIView):

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
        if check_editor_group(request):
            watchlist = self.get_object(pk)
            serializer = WatchListSerializer(watchlist, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({'error':True, 'message':'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, pk, format=None):
        if check_editor_group(request):
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


from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import mixins, viewsets
from random import randint

def generate_otp(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


# class VerifyCodeViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
#     # """
#     # Send verification code
#     # """
#     permission_classes = [AllowAny] # Allow everyone to register
    
#     serializer_class = OTPCodeSerializer # Related pre send verification logic
#     def generate_code(self):

#     # Generate 6 Digit verification code Prevent cracking
#     # :return:

#         seeds = "1234567890abcdefghijklmnopqrstuvwxyz"
#         random_str = []
#         for i in range(6):
#             random_str.append(choice(seeds))
#             return "".join(random_str)
#     def create(self, request, *args, **kwargs):
#         # Self defined create() The content of
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True) # This step is equivalent to verifying before sending
#         # from validated_data In order to get mobile
#         email = serializer.validated_data["email"]
#         # Random generation code
#         code = self.generate_code()
#         # Send SMS or email verification code
#         sms_status = SendVerifyCode.send_email_code(code=code, to_email_adress=email)
#         if sms_status == 0:
#           # Log
#           return Response({"msg": " Failed to send mail "}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             code_record = OTPCode(code=code, email=email)
#         # Save verification code
#             code_record.save()
#             return Response(
#             {"msg": f" The verification code has been sent to {email} Send complete "}, status=status.HTTP_201_CREATED
#             )



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

    def post(self, request):
        user = request.user
        otp_obj = OTPCode.objects.get(user=user)
        user_submitted_otp = request.POST.get('otp_code') 
        if otp_obj.code == user_submitted_otp:
            return Response(data={'message':'User verified'}, status=status.HTTP_200_OK)
        return Response(data={'message':'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
