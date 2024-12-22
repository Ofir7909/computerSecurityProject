from django.db import IntegrityError
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpRequest
from .forms import LoginForm, RegisterForm, ResetPasswordForm, ForgotPasswordForm
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

def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
    else:
        form = ForgotPasswordForm()
        return render(request, 'forgot_password.html', {'form': form})



def reset_password(request):
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            
            if new_password != confirm_password:
                return render(request, "reset_password.html", {    "form": form,   "error": "New password and confirmation do not match." })

            return render(request, "reset_password.html", { "form": form,  "success": "Password reset successful!"   })
        
        else:
            return render(request, "reset_password.html", {  "form": form,   "error": "Invalid data submitted!"   })
    
    else:
        form = ResetPasswordForm()
        return render(request, "reset_password.html", {"form": form})


