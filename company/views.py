from django.shortcuts import render, HttpResponse, redirect
from . models import CompanyCreationForm, CompanyLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from reusables.reusables import loginForm, signupForm, profileForm
from post.models import addPostForm, Post
from . models import Company
User = get_user_model()


@login_required(login_url="company:login")
def home(request):
    currentCompanyPosts = Post.objects.filter(
        company=getCurrentCompany(request))
    return render(request, 'company/home.html', {'posts': currentCompanyPosts})


@login_required(login_url="company:login")
def addPost(request):
    company = getCurrentCompany(request)

    formInitialData = {'company': company}
    form = addPostForm(initial=formInitialData)

    if request.method == 'POST':
        form = addPostForm(
            request.POST)
        if form.is_valid():

            form.save()
            return redirect('company:home')
    return render(request, 'company/addpost.html', {'form': form})


def viewProfile(request):
    compay = Company.objects.filter(user=request.user)
    fields = [(field.name, getattr(student[0], field.name))
              for field in Company._meta.get_fields() if field.name != 'id' and field.name != 'user' and field.name != 'profileCompleted']
    return render(request, 'company/profile.html', {'company': company[0], 'fields': fields})


@login_required(login_url="company:login")
def editProfile(request):
    return profileForm(request, 'company')


def companyLogin(request):
    return loginForm(request, 'company')


def signup(request):
    return signupForm(request, 'company')


@login_required(login_url="company:login")
def companyLogout(request):
    logout(request)
    return redirect('company:login')


def getCurrentCompany(request):
    try:
        return Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        return None
