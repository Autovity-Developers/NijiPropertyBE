from django.urls import include, path
from rest_framework import routers
# from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import RegisterAPI

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
# router.register(r'properties', views.PropertyListView)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api_list/', views.api_list, name='api_list'),
    path('api_list/login/', views.MyTokenObtainPairView.as_view()),
    path('api_list/properties/', views.PropertyList.as_view()),
    path('api_list/properties/create/', views.PropertyCreateView.as_view()),
    path('api_list/properties/<str:title>/', views.PropertyDetailView.as_view()),
    path('api_list/featured/', views.FeatureProperties.as_view()),
    path('api_list/premuim/', views.PremiumProperties.as_view()),
    path('api_list/property_type/', views.PropertyTypeListCreateView.as_view()),
    path('api_list/property_type/<str:type>/', views.PropertyTypeDetailView.as_view()),
    path('api_list/search/', views.SearchView.as_view()),
    path('api_list/post/', views.PostListCreateView.as_view()),
    path('api_list/post/<int:pk>/', views.PostDetailView.as_view()),
    path('api_list/contact/', views.ContactListCreateView.as_view()),
    path('api_list/contact/<int:pk>/', views.ContactDetailView.as_view()),
   
    path('api_list/map/', views.MapListCreateView.as_view()),
    path('api_list/map/<int:pk>/', views.MapDetailView.as_view()),
    path('api_list/bank/', views.BankListCreateView.as_view()),
    path('api_list/bank/<int:pk>/', views.BankDetailView.as_view()),
    path('api_list/newsblogs/', views.NewsBlogsListCreateView.as_view()),
    path('api_list/newsblogs/<int:pk>/', views.NewsBlogsDetailView.as_view()),
    path('api_list/images/', views.ImagesListCreateView.as_view()),
    path('api_list/images/<int:pk>/', views.ImagesDetailView.as_view()),
    path('api_list/watchlist/', views.WatchListCreateView.as_view()),
    path('api_list/watchlist/<int:pk>/', views.WatchlistDetailView.as_view()),
    
    path('api_list/card/', views.CardListCreateView.as_view()),
    path('api_list/card/<int:pk>/', views.CardDetailView.as_view()),
    path('api_list/about/', views.AboutListCreateView.as_view()),
    path('api_list/about/<int:pk>/', views.AboutDetailView.as_view()),

    path('api_list/register/', RegisterAPI.as_view(), name='register'),
    path('api_list/otp/', views.SendOTPView.as_view()),
    path('api_list/otp-verify/', views.VerifyOTPView.as_view()),

]

# urlpatterns = format_suffix_patterns(urlpatterns)

