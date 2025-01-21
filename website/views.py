from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpRequest
from .forms import LoginForm, RegisterForm, ResetPasswordForm, ForgotPasswordForm
from .models import User, Client
from django.conf import settings


def system(request):
    template = loader.get_template("system.html")
    clients = Client.objects.all()
    return render(request, "system.html", {"clients": clients})


def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render(request=request))


def login(request):
    if request.method == "GET":
        template = loader.get_template("login.html")
        form = LoginForm()
        return HttpResponse(template.render({"form": form}, request))
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if (
            user is not None
        ):  # https://stackoverflow.com/questions/16853044/logging-an-abstract-user-in
            return redirect("index")
        else:
            return render(
                request,
                "login.html",
                {"form": LoginForm(), "message": "Bad username or password"},
            )
    else:
        # return render(request, 'login.html')
        form = LoginForm(request.POST)
        print(form.data)
        return HttpResponse(form.data)


def register(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            if not settings.PASSWORD_REQUIERMENTS.is_password_valid(
                form.data["password"]
            ):
                form.add_error(None, "The password is not met the requirements")
            else:
                try:
                    user = User.objects.create_user(
                        form.data["username"], form.data["email"], form.data["password"]
                    )
                    return redirect("login")
                except IntegrityError:
                    form.add_error(None, "User already exists")
                # ERROR
    elif request.method == "GET":
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
    else:
        form = ForgotPasswordForm()
        return render(request, "forgot_password.html", {"form": form})


def reset_password(request):
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            current_password = form.cleaned_data["current_password"]
            new_password = form.cleaned_data["new_password"]
            confirm_password = form.cleaned_data["confirm_password"]

            if new_password != confirm_password:
                return render(
                    request,
                    "reset_password.html",
                    {
                        "form": form,
                        "error": "New password and confirmation do not match.",
                    },
                )

            return render(
                request,
                "reset_password.html",
                {"form": form, "success": "Password reset successful!"},
            )

        else:
            return render(
                request,
                "reset_password.html",
                {"form": form, "error": "Invalid data submitted!"},
            )

    else:
        form = ResetPasswordForm()
        return render(request, "reset_password.html", {"form": form})


def authenticate(username=None, password=None):
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None
