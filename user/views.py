from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth, messages

from django.urls import reverse
from django import forms

import time

def login(request):
    '''
    用户登陆
    显示登陆表单，时间，错误信息
    POST方法时作登陆验证
    '''
    curtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    error_message = ""

    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS, "Login Success.")
            return HttpResponseRedirect(reverse('polls:index'))
        messages.add_message(request, messages.SUCCESS, "Error username or password.")
    return render(request, "user/login.html", {'curtime':curtime})

def logout(request):
    '''
    用户登出
    '''
    auth.logout(request)
    messages.add_message(request, messages.SUCCESS, "Logout Success.")
    return HttpResponseRedirect(reverse('polls:index'))

class UserForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=20)
    password = forms.CharField(label='Password:', widget=forms.PasswordInput())
    email = forms.EmailField(label='Email:')

def register(request):
    '''
    用户注册
    显示注册表单
    如果为post请求，向user表写入登陆信息
    '''
    if request.method=='POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            email = uf.cleaned_data['email']
            print(username,password,email)

            user = User.objects.create_user(username,email,password)
            user.save()

            messages.add_message(request, messages.SUCCESS, "Register Success.Click 'Login'.")
            return HttpResponseRedirect(reverse('polls:index'))
    return render(request, "user/register.html")


            