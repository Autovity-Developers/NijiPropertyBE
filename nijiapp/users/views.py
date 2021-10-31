from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from django.contrib.auth.hashers import make_password
from .decorators import allowed_users

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:       
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.success(request,('Invalid username or password! '))
                return redirect('admin_login')
        else:
            if request.user.is_authenticated:
                return redirect('dashboard')
            return render(request, 'auth/login.html')



def change_admin_pw(request):
    if request.method == 'POST':
        name = request.user.username
        user = get_object_or_404(User, username=name)
        form = UserForm(request.POST or None)
        if form.is_valid():
            user.password=make_password(form.cleaned_data['password'])
            user.save() 
            messages.success(request, 'Password has been updated!')
            return redirect('admin_login')   
        else:
            messages(request, 'Failed to change password!')
            return redirect('change_admin_pw')

            
    elif request.method == 'GET':
        return render(request, 'auth/change_password.html')


def admin_logout(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('admin_login')

@login_required
def list_admins(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'auth/users/admins.html',context)

@login_required
def new_user(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('password1')
        cnPwd = request.POST.get('password2')
        try:
            if User.objects.filter(username__iexact=name).exists():
                msg = "A user with \'" + name + "\' username already exists!"
                messages.error(request, msg)
                return redirect('new_user')
            else:
                if pwd == cnPwd:
                    user = User(username = name)
                    user.set_password(cnPwd)
                    user.is_superuser=True
                    user.is_staff=True
                    user.email = request.POST.get('email')
                    user.save()
                    msg = "New user width \'" + name + "\' username created!"
                    messages.success(request, msg)
                    return redirect('list_admins')
                else:
                    messages.error(request, 'Password didn\'t matched!')
                    return render(request, 'auth/users/create.html',{'username':name})
        except:
            messages.error(request,'An error occured during user creation!')
            return redirect('add_user')
    else:
        return render(request, 'auth/users/create.html')


@login_required
def user_detail(request, pk):
    user = User.objects.get(pk=pk)
    context = {'user':user}
    return render(request, 'auth/users/detail.html', context)

@login_required
def update_user(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, "User email updated!")
        return redirect('list_admins')
    else:        
        context = {
            'current_user':user
            }
        return render(request, 'auth/users/update.html', context)


def delete_user(request, pk):
    user = User.objects.get(pk=pk)
    name = user.username
    user.delete()
    msg = "User with \'" + name + "\' name deleted!" 
    messages.success(request, msg)
    return redirect(list_admins)