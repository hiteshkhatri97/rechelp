from django.shortcuts import render, HttpResponse, redirect
from . models import StudentCreationForm, StudentLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from reusables.reusables import loginForm, signupForm, profileForm, connectDatabase
from post.models import Post
from company.models import Company
from . models import Student
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from pymongo import MongoClient
import datetime

User = get_user_model()


@login_required(login_url="student:login")
def home(request):
    posts = Post.objects.all()
    companys = Company.objects.all()
    student = Student.objects.filter(user=request.user)
    appliedPosts = getAppliedPosts(student[0].id)

    if request.GET.get('viewprofile') == 'viewprofile':
        return viewOutsideProfile(request, int(request.GET.get('companyid')))

    if request.GET.get('apply') == 'apply':
        appliedStudents(request.GET.get('postid'),
                        request.GET.get('studentid'))
        return redirect('student:home')
    return render(request, 'student/home.html', {'posts': posts, 'companys': companys, 'student': student[0].id, 'appliedPosts':
                                                 appliedPosts, 'today': datetime.date.today()})


def viewProfile(request):
    student = Student.objects.filter(user=request.user)
    fields = [(field.name, getattr(student[0], field.name))
              for field in Student._meta.get_fields() if field.name != 'id' and field.name != 'user' and field.name != 'profileCompleted']
    return render(request, 'student/profile.html', {'student': student[0], 'fields': fields})


@login_required(login_url="student:login")
def editProfile(request):
    student = Student.objects.filter(user=request.user)
    instance = student[0] if student[0].profileCompleted else None
    return profileForm(request, 'student', instance)


def studentLogin(request):
    return loginForm(request, 'student')


def signup(request):
    return signupForm(request, 'student')


@login_required(login_url="student:login")
def studentLogout(request):
    logout(request)
    return redirect('student:login')


def appliedStudents(postId, studentId):

    collection = connectDatabase()

    cursor = list(collection.find({"id": int(postId)}, {
                  "appliedStudents": 1, '_id': 0}))[0]['appliedStudents']

    if int(studentId) not in cursor:
        cursor.append(int(studentId))

    result = collection.update(
        {'id': int(postId)}, {'$set': {'appliedStudents': cursor}})


def getAppliedPosts(studentId):
    collection = connectDatabase()

    cursor = [id['id'] for id in list(collection.find({'appliedStudents': int(studentId)}, {
        "id": 1, '_id': 0}))]
    return cursor


def viewOutsideProfile(request, companyid):
    company = Company.objects.filter(id=companyid)
    fields = [(field.name, getattr(company[0], field.name))
              for field in Company._meta.get_fields() if field.name != 'post' and field.name != 'id' and field.name != 'user' and field.name != 'profileCompleted']
    return render(request, 'company/profile.html', {'company': company[0], 'fields': fields})
