from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth, messages

from django.urls import reverse
from django import forms

from .models import Question
import time


def index(request):
    '''
    首页
    '''
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list,}
    return render(request, 'polls/index.html', context)

@login_required(login_url='polls:login')
def detail(request, question_id):
    '''
    投票详细页
    内有投票名和投票选项
    '''
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/details.html', {'question':question})

@login_required(login_url='polls:login')
def results(request, question_id):
    '''
    投票结果
    '''
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})

@login_required(login_url='polls:login')
def vote(request, question_id):
    '''
    用户在detail中点击投票后向vote发送请求
    对投票table处理完成后重定向至results页
    '''
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError):
        # 重新展示投票页面
        return render(request, 'polls/details.html', {
            'question':question,
            'error_message':"You didn't select a choice."})
    else:
        selected_choice.votes +=1
        selected_choice.save()
        # 在成功处理一次POST数据之后返回一个HttpResponseRedirect
        # 这样可以防止用户点击返回按钮的时候重复提交
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

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
    return render(request, "polls/login.html", {'curtime':curtime})

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
    return render(request, "polls/register.html")


            