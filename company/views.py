from django.shortcuts import render, HttpResponse, redirect
from . models import CompanyCreationForm, CompanyLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from reusables.reusables import loginForm, signupForm, profileForm, connectDatabase
from post.models import addPostForm, Post
from . models import Company
from student.models import Student
import datetime
User = get_user_model()


@login_required(login_url="company:login")
def home(request):

    currentCompanyPosts = Post.objects.filter(
        company=getCurrentCompany(request))
    postDatesSet = set([post.postDate for post in currentCompanyPosts])

    if request.GET.get('delete') == 'delete':
        deletePost(request.GET.get('postid'))
        return redirect('company:home')
    if request.GET.get('appliedstudents') == 'applied students':
        return appliedStudents(request)

    if request.GET.get('viewprofile') == 'viewprofile':
        return viewOutsideProfile(request, int(request.GET.get('studentid')))

    return render(request, 'company/home.html', {'posts': enumerate(currentCompanyPosts), 'postDatesSet': postDatesSet})


@login_required(login_url="company:login")
def addPost(request):
    company = getCurrentCompany(request)
    if company.profileCompleted == False:
        return redirect('company:editprofile')

    formInitialData = {'company': company}
    form = addPostForm(initial=formInitialData)

    if request.method == 'POST':
        form = addPostForm(
            request.POST)
        if form.is_valid():

            newPost = form.save()

            collection = connectDatabase()

            result = collection.update(
                {'id': int(newPost.id)}, {'$set': {'appliedStudents': []}})

            return redirect('company:home')
    return render(request, 'company/addpost.html', {'form': form})


def viewProfile(request):
    company = Company.objects.filter(user=request.user)
    fields = [(field.name, getattr(company[0], field.name))
              for field in Company._meta.get_fields() if field.name != 'post' and field.name != 'id' and field.name != 'user' and field.name != 'profileCompleted']
    return render(request, 'company/profile.html', {'company': company[0], 'fields': fields})


@login_required(login_url="company:login")
def editProfile(request):
    company = Company.objects.filter(user=request.user)
    instance = company[0] 
    return profileForm(request, 'company', instance)


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


def deletePost(postId):
    Post.objects.filter(id=postId).delete()


def appliedStudents(request):
    postid = request.GET.get('postid')
    print(postid, type(postid))
    post = Post.objects.filter(id=postid)
    collection = connectDatabase()
    result = list(collection.find({'id': int(postid)}, {
        'appliedStudents': 1, '_id': 0}))[0]['appliedStudents']
    students = []
    if len(result) > 0:
        print('in if')
        for id in result:
            print(Student.objects.filter(id=int(id))[0])
        students = [Student.objects.filter(id=int(id))[0] for id in result]
    print(students)
    return render(request, 'company/appliedstudents.html', {'students': students})


def viewOutsideProfile(request, studentid):
    student = Student.objects.filter(id=studentid)
    details = [(field.name, getattr(student[0], field.name))
               for field in Student._meta.get_fields() if field.name == 'enrollmentNumber' or field.name == 'fieldsOfInterest']
    marks = [(field.name.replace("Marks", ""), getattr(student[0], field.name)) for field in Student._meta.get_fields() if field.name ==
             'wtMarks' or field.name == 'androidMarks' or field.name == 'iosMarks' or field.name == 'javaMarks' or field.name == 'pythonMarks' or field.name == 'cpi' or field.name == 'aptitude']
    return render(request, 'company/outsideprofile.html', {'marks': marks, 'details': details, 'student': student[0]})
