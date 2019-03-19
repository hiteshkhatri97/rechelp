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
        collection = connectDatabase()
        # logic for getting applied students and passing it to display
    return render(request, 'company/home.html', {'posts': enumerate(currentCompanyPosts), 'postDatesSet': postDatesSet})


@login_required(login_url="company:login")
def addPost(request):
    company = getCurrentCompany(request)

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
    instance = company[0] if company[0].profileCompleted else None
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
