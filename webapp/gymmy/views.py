from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request, "gymmy/landing.html", {})

def about(request):
    return render(request, 'gymmy/aboutpage.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome Back! {username}')
            return redirect('homepage')
        else:
            return redirect('login')
    else:
        return render(request, 'gymmy/login.html', {})

def signup_user(request):
    form = UserRegisterForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('login')
    else:
        form = UserRegisterForm()

    context = {'form':form}
    return render(request, 'gymmy/signup.html', context) 
        
def logout_user(request):
    logout(request)
    return redirect('homepage')
