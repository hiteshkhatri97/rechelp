from django.shortcuts import render, HttpResponse, redirect
from . models import StudentCreationForm, StudentLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from reusables.reusables import loginForm, signupForm, profileForm
from post.models import Post
from . models import Student
User = get_user_model()


@login_required(login_url="student:login")
def home(request):
    posts = Post.objects.all()
    return render(request, 'student/home.html', {'posts': posts})


def viewProfile(request):
    student = Student.objects.filter(user=request.user)
    fields = [(field.name, getattr(student[0], field.name))
              for field in Student._meta.get_fields() if field.name != 'id' and field.name != 'user' and field.name != 'profileCompleted']
    return render(request, 'student/profile.html', {'student': student[0], 'fields': fields})


@login_required(login_url="student:login")
def editProfile(request):
    return profileForm(request, 'student')


def studentLogin(request):
    return loginForm(request, 'student')


def signup(request):
    return signupForm(request, 'student')


@login_required(login_url="student:login")
def studentLogout(request):
    logout(request)
    return redirect('student:login')
