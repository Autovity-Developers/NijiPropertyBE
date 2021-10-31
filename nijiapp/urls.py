from django.conf import settings
from django.conf.urls.static import static
from .import views
from django.urls import path

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)