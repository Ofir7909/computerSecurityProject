from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .forms import LoginForm
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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None: #https://stackoverflow.com/questions/16853044/logging-an-abstract-user-in
            return render(request, 'login.html', 
                {'message': 'Login Successfully'})
        else:
            return render(request, 'login.html', 
                {'message': 'Bad username or password'})
    else:
        #return render(request, 'login.html')
        form = LoginForm(request.POST)
        print(form.data)
        return HttpResponse(form.data)


def register(request):
    template = loader.get_template("register.html")
    return HttpResponse(template.render(request=request))


def reset_password(request):
    template = loader.get_template("reset_password.html")
    return HttpResponse(template.render(request=request))

def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None


    