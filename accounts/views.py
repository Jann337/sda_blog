from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import User

# Create your views here.


def registration(request):
    if request.method == "POST":
        username = request.POST.get("username")
        pw = request.POST.get("password")
        pw2 = request.POST.get("password2")

        if pw != pw2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if len(username) < 4:
            messages.error(request, "Username must be at least 4 characters")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        User.objects.create_user(username=username, password=pw)

    return render(request, "registration/register.html")
