from company.models import CompanyLoginForm, CompanyCreationForm, CompanyProfileForm, Company
from student.models import StudentLoginForm, StudentCreationForm, StudentProfileForm, Student
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from pymongo import MongoClient
from django.contrib import messages
User = get_user_model()


def loginForm(request, user_type):

    form = StudentLoginForm() if user_type == 'student' else CompanyLoginForm()
    if request.method == 'POST':
        form = StudentLoginForm(
            data=request.POST) if user_type == 'student' else CompanyLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user and user.userType == user_type:
                login(request, user)
                return redirect(user_type + ':home')
            else:
                messages.success(request, "Error")

    return render(request, user_type + '/login.html', {'form': form})


def signupForm(request, user_type):

    form = StudentCreationForm() if user_type == 'student' else CompanyCreationForm()
    if request.method == 'POST':
        form = StudentCreationForm(
            request.POST) if user_type == 'student' else CompanyCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user_type == 'student':
                Student.objects.create(user=user)
            else:
                Company.objects.create(user=user)
            login(request, user)
            return redirect(user_type + ':editprofile')
    return render(request, user_type + '/signup.html', {'form': form})


def profileForm(request, user_type, instance):
    form = None
    formInitialData = {'user': request.user, 'profileCompleted': True}
    studentFormInitialData = {'user': request.user,
                              'profileCompleted': True, 'picture': 'default.png'}
    if instance is None:
        form = StudentProfileForm(
            initial=studentFormInitialData, instance=instance) if user_type == 'student' else CompanyProfileForm(initial=formInitialData, instance=instance)
    else:
        print('instance')
        form = StudentProfileForm(
            initial=studentFormInitialData, instance=instance) if user_type == 'student' else CompanyProfileForm(initial=formInitialData, instance=instance)

    if request.method == 'POST':
        print(instance)
        form = StudentProfileForm(
            request.POST, request.FILES,instance=instance) if user_type == 'student' else CompanyProfileForm(request.POST, instance=instance)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect(user_type + ':home')
    return render(request, user_type + '/editprofile.html', {'form': form})


def connectDatabase():
    conn = None
    try:
        conn = MongoClient()
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    db = conn.rechelp
    collection = db.post_post

    return collection
