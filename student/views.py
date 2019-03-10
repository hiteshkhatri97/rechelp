from django.shortcuts import render, HttpResponse, redirect
from . models import StudentCreationForm, StudentLoginForm
from django.contrib import messages
from django.contrib.auth import  login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
User = get_user_model()

@login_required(login_url="student:login")
def home(request):
    return render(request, 'student/home.html')
    

def profile(request):
    return render(request, 'student/profile.html')


def studentLogin(request):
    if request.method == 'POST':
        studentLoginForm = StudentLoginForm(data=request.POST)
        if studentLoginForm.is_valid():
            user = studentLoginForm.get_user()
            if user:
                login(request, user)
        return redirect('student:home')
    else:
        studentLoginForm = StudentLoginForm()
    return render(request, 'student/login.html', {'studentLoginForm': studentLoginForm})

def signup(request):
    if request.method == 'POST':
        studentCreationForm = StudentCreationForm(request.POST)
        if studentCreationForm.is_valid():
            studentCreationForm.save()
            username = studentCreationForm.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('student:profile')
    else:
        studentCreationForm = StudentCreationForm()
    return render(request, 'student/signup.html', {'studentCreationForm': studentCreationForm})


def studentLogout(request):
    logout(request)
    message = "logout successful"
    return redirect('student:login')


# def login(request):
#     if request.method == 'POST':
#         studentLoginForm = StudentLoginForm(request.POST)
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         userType = request.POST.get('userType')
#         user = authenticate(username = username, password = password, userType = userType)
#         if user:
#             login(request)
#             return redirect('home')
#     else:
#         studentLoginForm = StudentLoginForm()
#     return render(request, 'student/login.html', {'studentLoginForm': studentLoginForm})


