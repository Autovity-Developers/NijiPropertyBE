from  django.urls import path
from .import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name = 'admin_logout'),
    path('change-admin-password/', views.change_admin_pw, name='change_admin_pw'),
    path('users/new/', views.new_user, name = 'new_user'),
    path('users/admins/', views.list_admins, name= 'list_admin'),
    path('users/detail/<str:pk>/', views.user_detail, name='user_detail'),
    path('users/update/<str:pk>/', views.update_user, name='update_user'),
    path('user/delete/<str:pk>/', views.delete_user, name='delete_user'),
    

]