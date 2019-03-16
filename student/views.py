from django.shortcuts import render, HttpResponse, redirect
from . models import StudentCreationForm, StudentLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from reusables.reusables import loginForm, signupForm, profileForm
User = get_user_model()


@login_required(login_url="student:login")
def home(request):
    return render(request, 'student/home.html')


@login_required(login_url="student:login")
def profile(request):
    return profileForm(request, 'student')


def studentLogin(request):
    return loginForm(request, 'student')


def signup(request):
    return signupForm(request, 'student')


@login_required(login_url="student:login")
def studentLogout(request):
    logout(request)
    return redirect('student:login')
