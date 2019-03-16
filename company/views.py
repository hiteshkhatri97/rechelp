from django.shortcuts import render, HttpResponse, redirect
from . models import CompanyCreationForm, CompanyLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from reusables.reusables import loginForm, signupForm
User = get_user_model()


@login_required(login_url="company:login")
def home(request):
    return render(request, 'company/home.html')


def profile(request):
    return render(request, 'company/profile.html')


def companyLogin(request):
    return loginForm(request, 'company')


def signup(request):
    return signupForm(request, 'company')
    companyCreationForm = CompanyCreationForm()


def companyLogout(request):
    logout(request)
    return redirect('company:login')
