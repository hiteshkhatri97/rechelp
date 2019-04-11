from django.shortcuts import render, HttpResponse, redirect
from . models import StudentCreationForm, StudentLoginForm, GraduatedStudentForm
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
    companys = [Company.objects.filter(id = post['company_id']).first() for post in posts.values('company_id').distinct()]
    student = Student.objects.filter(user=request.user)
    appliedPosts = getAppliedPosts(student[0].id)

    if request.GET.get('viewprofile') == 'viewprofile':
        return viewOutsideProfile(request, int(request.GET.get('companyid')))

    if request.GET.get('apply') == 'apply':
        print(student[0])
        if student[0].profileCompleted == False:
            return redirect('student:editprofile')
        appliedStudents(request.GET.get('postid'),
                        request.GET.get('studentid'))
        return redirect('student:home')

    if request.GET.get('showresult') == 'showresult':
        return showResult(request, request.GET.get('postid'),  request.GET.get('studentid'))

    if request.GET.get('predict') == 'predict':
        return predict(request)

    return render(request, 'student/home.html', {'posts': posts, 'companys': companys, 'student': student[0].id, 'appliedPosts':
                                                 appliedPosts, 'today': datetime.date.today()})


def viewProfile(request):
    student = Student.objects.filter(user=request.user)
    details = [(field.name, getattr(student[0], field.name))
               for field in Student._meta.get_fields() if field.name == 'enrollmentNumber' or field.name == 'fieldsOfInterest']
    marks = [(field.name.replace("Marks", ""), getattr(student[0], field.name)) for field in Student._meta.get_fields(
    ) if 'Marks' in field.name or field.name == 'cpi' or field.name == 'aptitude']
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


def showResult(request, postid, studentid):
    collection = connectDatabase()

    cursor = list(collection.find({'id': int(postid)}, {
                  "selectedStudents": 1, '_id': 0}))[0]['selectedStudents']
    message, error_message = '', ''
    if int(studentid) in cursor:
        message = 'Congratulations you are selected :)'
    else:
        error_message = 'Sorry you are not selected :('
    return render(request, 'student/showresult.html', {'message': message, 'errormessage': error_message})


def predict(request):
    student = Student.objects.filter(id=int(request.GET.get('studentid')))[0]
    technology = request.GET.get('posttechnology')
    companyid = request.GET.get('companyid')
    fieldtoselect = [
        field.name for field in Student._meta.get_fields() if technology.replace('Marks', '') in field.name][0]
    markk = getattr(student, fieldtoselect)
    aptitude = student.aptitude
    cpii = student.cpi

    exceldir = os.path.realpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__)))
    excel = os.path.join(exceldir, 'lr.xlsx')
    data = pd.read_excel(excel, sheet_name="Sheet1")
    cpi = data['cpi']
    apti = data['aptitude']
    rec = data['recruited']
    wtMarks = data['wtMarks']
    androidMarks = data['androidMarks']
    iosMarks = data['iosMarks']
    javaMarks = data['javaMarks']
    pythonMarks = data['pythonMarks']
    selectedTechnology = data['selectedTechnology']
    company = columns = data['company']
    marks = {'wt': wtMarks, 'android': androidMarks,
             'ios': iosMarks, 'java': javaMarks, 'python': pythonMarks}

    X = pd.DataFrame({'cpi': cpi,
                      'marks': marks[technology], 'apti': apti, 'company': company})
    Y = pd.DataFrame({'rec': data['recruited']})

    X_train, x_test, Y_train, y_test = train_test_split(
        X, Y, test_size=0.2)

    classifier = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)

    classifier.fit(X_train, Y_train)

    apple = np.array([cpii, markk, aptitude,companyid]).reshape(1, 4)
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

    return render(request, 'student/predictionresult.html', {'message': message, 'errormessage': error_message})


def graduatedStudent(request):

    form = GraduatedStudentForm()
    if request.method == 'POST':
        form = GraduatedStudentForm(request.POST)
        if form.is_valid:
            try:
                exceldir = os.path.realpath(os.path.join(
                    os.getcwd(), os.path.dirname(__file__)))
                excel = os.path.join(exceldir, 'lr.xlsx')
                data = pd.read_excel(excel, sheet_name="Sheet1")

                firstNamme = request.POST.get("firstName")
                lastName = request.POST.get("lastName")
                cpi = float(request.POST.get("cpi"))
                aptitude = request.POST.get("aptitude")
                wtMarks = request.POST.get("wtMarks")
                androidMarks = request.POST.get("androidMarks")
                iosMarks = request.POST.get("iosMarks")
                javaMarks = request.POST.get("javaMarks")
                pythonMarks = request.POST.get("pythonMarks")
                recruited = request.POST.get("recruited")
                selectedTechnology = request.POST.get("selectedTechnology")
                company = request.POST.get("company")

                n = len(data)

                data.loc[n] = (firstName, lastName, cpi, aptitude, wtMarks, androidMarks,
                               iosMarks, javaMarks, pythonMarks, selectedTechnology, company, recruited)
                data.to_excel(excel, sheet_name="Sheet1")
                message = "Data entry successful"
                return render(request, 'student/gradutedstudent.html', {'message': message})

            except Exception as e:
                print(e)
                error_message = "Please try again"
                return render(request, 'student/gradutedstudent.html', {'errormessage': error_message, 'form': form})

    return render(request, 'student/gradutedstudent.html', {'form': form})
