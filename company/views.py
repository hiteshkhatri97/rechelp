from django.shortcuts import render, HttpResponse


def home(request):
    return render(request,'company/home.html')

def profile(request):
    return render(request, 'company/profile.html')

def login(request):
    return render(request, 'company/login.html')

def signup(request):
    return render(request, 'company/signup.html')
