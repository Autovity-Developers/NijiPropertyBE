from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from rest_framework import generics
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from django.views import View
from django.forms.models import modelformset_factory
from django.template import RequestContext
import os

# Create your views here.

@login_required
def dashboard(request):
    # business_title = SliderHome.objects.all()
    # context = {'business_title': business_title}
    return render(request, 'dashboard/dashboard.html')