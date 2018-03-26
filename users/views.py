from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import User


# Create your views here.
def index(request):
    return render(request, "users/login.html")


def signup(request):
    ctx = {}
    if request.POST:
        ctx['username'] = request.POST['name_username']
        ctx['password'] = request.POST['name_password']
        ctx['email'] = request.POST['name_email']
    return render(request, "users/login.html", ctx)

