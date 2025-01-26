from datetime import timedelta
from django.utils import timezone
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from website.email import send_email
from .forms import (
    LoginForm,
    RegisterForm,
    ResetPasswordForm,
    ForgotPasswordForm,
    ClientForm,
)
from .models import PasswordHistory, Token, User, Client
from django.conf import settings
from django.db.models import Q
from django.utils.html import escape
from .hashers import MyPBKDF2PasswordHasher


@login_required(login_url="/login")
def system(request):
    filter_query = request.GET.get("filter", "").strip()

    if filter_query:
        filter_query = escape(filter_query)
        clients = Client.objects.filter(
            Q(id__icontains=filter_query) | Q(name__icontains=filter_query)
        )
    else:
        clients = Client.objects.all()

    return render(request, "system.html", {"clients": clients})


@login_required(login_url="/login")
def create_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            Client.objects.create(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
            )
            return redirect("system")
    else:
        form = ClientForm()
    return render(request, "create_client.html", {"form": form})


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
        if form.is_valid():
            my_hasher = MyPBKDF2PasswordHasher()
            hashed_password = my_hasher.encode(form.data["password"], my_hasher.salt())

            user = User.objects.raw(
                f"SELECT * from website_user where username='{form.data['username']}' and password='{hashed_password}'"
            )

            user = user[0] if len(user) > 0 else None

            # https://stackoverflow.com/questions/16853044/logging-an-abstract-user-in
            if user is not None:
                django_login(request, user, backend="axes.backends.AxesBackend")
                return redirect("system")
            else:
                form.add_error(None, "Bad username or password")
        return render(request, "login.html", {"form": form})


def register(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            password_validation_error = (
                settings.PASSWORD_REQUIERMENTS.is_password_valid(form.data["password"])
            )
            if password_validation_error:
                form.add_error("password", password_validation_error)
            else:
                try:
                    user = User.objects.create_user(
                        form.data["username"], form.data["email"], form.data["password"]
                    )
                    PasswordHistory(password=user.password, user=user).save()

                    return redirect("login")
                except IntegrityError:
                    form.add_error(None, "This user already exists")

    elif request.method == "GET":
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            toMail = form.data["email"]
            try:
                user = User.objects.get(email=toMail)
            except User.DoesNotExist:
                form.add_error(None, "Mail doesn't Exist")
                return render(request, "forgot_password.html", {"form": form})
            token = Token(
                token=Token.generate_random_sha1_token(),
                user=user,
                expires_at=timezone.now() + timedelta(minutes=15),
            )
            token.save()
            send_email(toMail, "Test1", f"your Token is {token.token}")
            return redirect("reset_password")
    else:
        form = ForgotPasswordForm()
        return render(request, "forgot_password.html", {"form": form})


def reset_password(request):
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            token = form.cleaned_data["token"]
            new_password = form.cleaned_data["new_password"]
            confirm_password = form.cleaned_data["confirm_password"]

            if new_password != confirm_password:
                form.add_error("confirm_password", "Passwords do not match.")
                return render(request, "reset_password.html", {"form": form})
            try:
                token_obj = Token.objects.get(token=token)
            except Token.DoesNotExist:
                form.add_error("token", "Unknown token.")
                return render(request, "reset_password.html", {"form": form})

            if not token_obj.is_valid():
                form.add_error("token", "This token is expired")
                return render(request, "reset_password.html", {"form": form})

            password_validation_error = (
                settings.PASSWORD_REQUIERMENTS.is_password_valid(
                    form.data["new_password"]
                )
            )
            if password_validation_error:
                form.add_error("new_password", password_validation_error)
                return render(request, "reset_password.html", {"form": form})
            if PasswordHistory.is_in_history(token_obj.user, new_password):
                form.add_error("new_password", "Can't use an old password")
                return render(request, "reset_password.html", {"form": form})
            token_obj.user.set_password(new_password)
            token_obj.user.save()
            PasswordHistory(
                password=token_obj.user.password, user=token_obj.user
            ).save()
            return redirect("login")
        else:
            return render(
                request,
                "reset_password.html",
                {"form": form, "error": "Invalid data submitted!"},
            )

    else:
        form = ResetPasswordForm()
        return render(request, "reset_password.html", {"form": form})
