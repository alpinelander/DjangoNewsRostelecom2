from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from .models import *
from .forms import *

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group

from django.contrib.auth.decorators import login_required
def profile_update(request):
    user = request.user
    account = Account.objects.get(user=user)
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        account_form = AccountUpdateForm(request.POST, request.FILES, instance=account)
        context = {'account_form': AccountUpdateForm(instance=account),
                   'user_form': UserUpdateForm(instance=user)}
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()

            messages.success(request,"Профиль успешно обновлен")
            return redirect('profile')
        else:
            error_dict= dict(account_form.errors)
            error_dict.update(dict(user_form.errors))
            messages.warning(request, error_dict)
    else:
        context = {'account_form':AccountUpdateForm(instance=account),
                   'user_form':UserUpdateForm(instance=user)}
    return render(request,'users/edit_profile.html',context)


@login_required
def profile_delete(request):
    user = request.user
    user.delete()
    return redirect('news')

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
def password_update(request):
    user = request.user
    form = PasswordChangeForm(user,request.POST)
    if request.method == 'POST':
        if form.is_valid():
            password_info = form.save()
            update_session_auth_hash(request,password_info)
            messages.success(request,'Пароль успешно изменен')
            return redirect('profile')

    context = {"form": form}
    return render(request,'users/edit_password.html',context)
def profile(request):
    context = dict()
    return render(request,'users/profile.html',context)
def registration(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() #появляется новый пользователь
            category = request.POST['account_type']
            if category == 'author':
                group = Group.objects.get(name='Actions Required')
                user.groups.add(group)
            else:
                group = Group.objects.get(name='Reader')
                user.groups.add(group)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            account = Account.objects.create(user=user,nickname=user.username)
            user = authenticate(username=username,password=password)
            login(request,user)
#            messages.success(request,f'{username} был зарегистрирован!')

            return redirect('home')
    else:
        form = UserCreationForm()
    context = {'form':form}
    return render(request,'users/registration.html',context)
# Create your views here.
def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print('Сообщение отправлено', form.cleaned_data)
        else:
            print(form.errors)
    else:
        form = ContactForm()
        form.name='Любимый клиент'
    context = {'form': form}
    return render(request,'users/contact_page.html',context)

def index(request):
    print(request.user,request.user.id)
    user_acc = Account.objects.get(user=request.user)
    print(user_acc, user_acc.birthdate, user_acc.gender)
    return HttpResponse('Приложение Users')
