from django.shortcuts import render, HttpResponse, redirect
from . models import CompanyCreationForm, CompanyLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
User = get_user_model()

@login_required(login_url="company:login")
def home(request):
    return render(request,'company/home.html')

def profile(request):
    return render(request, 'company/profile.html')

def companyLogin(request):
    if request.method == 'POST':
        companyLoginForm = CompanyLoginForm(data=request.POST)
        if companyLoginForm.is_valid():
            user = companyLoginForm.get_user()
            if user:
                login(request, user)
        return redirect('company:home')
    else:
        companyLoginForm = CompanyLoginForm()
    return render(request, 'company/login.html', {'companyLoginForm': companyLoginForm})

def signup(request):
    if request.method == 'POST':
        companyCreationForm = CompanyCreationForm(request.POST)
        if companyCreationForm.is_valid():
            companyCreationForm.save()
            username = companyCreationForm.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('company:profile')
    else:
        companyCreationForm = CompanyCreationForm()
    return render(request, 'company/signup.html', {'companyCreationForm': companyCreationForm})


def companyLogout(request):
    logout(request)
    message = "logout successful"
    return redirect('company:login')
