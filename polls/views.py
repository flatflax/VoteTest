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

@login_required(login_url='user:login')
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

@login_required(login_url='user:login')
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
  