from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .forms import LoginForm


def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render(request=request))


def login(request):
    if request.method == "GET":
        template = loader.get_template("login.html")
        form = LoginForm()
        return HttpResponse(template.render({"form": form}, request))
    elif request.method == "POST":
        form = LoginForm(request.POST)
        print(form.data)
        return HttpResponse(form.data)


def register(request):
    template = loader.get_template("register.html")
    return HttpResponse(template.render(request=request))


def reset_password(request):
    template = loader.get_template("reset_password.html")
    return HttpResponse(template.render(request=request))
