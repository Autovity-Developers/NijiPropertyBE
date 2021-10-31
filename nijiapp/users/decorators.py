from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages


def allowed_users (allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            # print("Working: ", allowed_roles)
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                # return HttpResponse("Only admin are allowed to view user details")
                messages.error(request, "Only admin are allowed to view user details")
                return redirect('dashboard')
        return wrapper_func
    return decorator