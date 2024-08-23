from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def home(response):
    return render(response, "gymmy/landing.html", {})

def about(response):
    return render(response, 'gymmy/aboutpage.html', {})

def login(response):
    return render(response, 'gymmy/login.html', {})

def signup(response):
    return render(response, 'gymmy/signup.html', {})

