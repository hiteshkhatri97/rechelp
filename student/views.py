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
import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from matplotlib.colors import ListedColormap
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
    if request.GET.get('predict') == 'predict':
        return predict(request)

    return render(request, 'student/home.html', {'posts': posts, 'companys': companys, 'student': student[0].id, 'appliedPosts':
                                                 appliedPosts, 'today': datetime.date.today()})


def viewProfile(request):
    student = Student.objects.filter(user=request.user)
    details = [(field.name, getattr(student[0], field.name))
               for field in Student._meta.get_fields() if field.name == 'enrollmentNumber' and field.name == 'fieldsfieldsOfInterestfieldsOfInterestOfInterest']
    print(details)
    marks = [(field.name.replace("Marks",""), getattr(student[0], field.name)) for field in Student._meta.get_fields() if field.name ==
             'wtMarks' and field.name == 'androidMarks' and field.name == 'iosMarks' and field.name == 'javaMarks' and field.name == 'pythonMarks' and field.name == 'cpi' and field.name == 'aptitude']
    print(marks)
    return render(request, 'student/profile.html', {'marks': marks, 'details': details, 'student': student[0]})


@login_required(login_url="student:login")
def editProfile(request):
    student = Student.objects.filter(user=request.user)
    instance = student[0]
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
    return render(request, 'student/outsideprofile.html', {'company': company[0], 'fields': fields})


def predict(request):
    student = Student.objects.filter(id=int(request.GET.get('studentid')))[0]
    technology = request.GET.get('posttechnology')
    fieldtoselect = [
        field.name for field in Student._meta.get_fields() if technology.replace('Marks', '') in field.name][0]
    markk = getattr(student, fieldtoselect)
    aptitude = student.aptitude
    cpii = student.cpi
    print(markk, aptitude, cpii)

    exceldir = os.path.realpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__)))
    excel = os.path.join(exceldir, 'lr.xlsx')
    data = pd.read_excel(excel, sheet_name="Sheet1")
    cpi = data['cpi']
    marks = data['marks']
    apti = data['aptitude']
    rec = data['recruited']
    X = pd.DataFrame({'cpi': data['cpi'],
                      'marks': data['marks'], 'apti': data['aptitude']})
    Y = pd.DataFrame({'rec': data['recruited']})

    X_train, x_test, Y_train, y_test = train_test_split(
        X, Y, test_size=0.2)

    model = LinearRegression()
    classifier = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)

    model.fit(X_train, Y_train)
    classifier.fit(X_train, Y_train)

    accuracy = model.score(x_test, y_test)

    apple = np.array([cpii, markk, aptitude]).reshape(1, 3)

    predictedresult = model.predict(apple)
    prediction = classifier.predict(apple)
    message, error_message = '', ''
    studentname = student.firstName + ' ' + student.lastName
    companyname = request.GET.get('companyname')
    if(int(prediction) == 1):
        message = 'Congratulations ' + studentname + ', you might get placed in ' + \
            companyname + ' as ' + technology + ' developer :)'

    else:
        error_message = 'Sorry ' + studentname + ', you should work harder to get placed in ' + \
            companyname + ' as ' + technology + ' developer :('

    l = len(data)
    n = l + 1
    if accuracy >= 0.8:
        data.loc[n] = (cpii, markk, aptitude, round(pree))
        data.to_excel(excel, sheet_name="Sheet1")
    return render(request, 'student/predictionresult.html', {'message': message, 'errormessage': error_message})
