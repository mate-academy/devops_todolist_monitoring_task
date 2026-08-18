from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from prometheus_client import Counter, generate_latest

from accounts.forms import LoginForm, RegistrationForm
from lists.forms import TodoForm
http_requests_total = Counter('http_requests_total', 'Total HTTP requests', ['method'])

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=request.POST["username"], password=request.POST["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("lists:index")
        else:
            return render(request, "accounts/login.html", {"form": form})
    else:
        return render(request, "accounts/login.html", {"form": LoginForm()})

    return redirect("lists:index")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=request.POST["username"],
                email=request.POST["email"],
                password=request.POST["password"],
            )
            return redirect("auth:login")
        else:
            return render(request, "accounts/register.html", {"form": form})
    else:
        return render(request, "accounts/register.html", {"form": RegistrationForm()})


def logout_view(request):
    logout(request)
    return redirect("lists:index")

@csrf_exempt
def metrics(request):
    http_requests_total.labels(method=request.method).inc()
    return HttpResponse(generate_latest(), content_type='text/plain')