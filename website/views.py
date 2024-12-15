from django.db import IntegrityError
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpRequest
from .forms import LoginForm, RegisterForm
from .models import User


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


def register(request: HttpRequest):
    register_template = loader.get_template("register.html")
    if request.method == "GET":
        form = RegisterForm()
        return HttpResponse(register_template.render({"form": form}, request))

    elif request.method == "POST":
        form = RegisterForm(request.POST)

        if not form.is_valid():
            return HttpResponse(register_template.render({"form": form}, request))

        try:
            user = User.objects.create_user(
                form.data["username"], form.data["email"], form.data["password"])
        except IntegrityError:
            form.add_error(None, "User already exists")
            return HttpResponse(register_template.render({"form": form}, request))

        return HttpResponse("user created successfully")


def reset_password(request):
    template = loader.get_template("reset_password.html")
    return HttpResponse(template.render(request=request))
