from django.shortcuts import render, HttpResponse, redirect
from . models import StudentCreationForm, StudentLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from reusables.reusables import loginForm, signupForm, profileForm
from post.models import Post
from company.models import Company
from . models import Student
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME

User = get_user_model()


@login_required(login_url="student:login")
def home(request):
    posts = Post.objects.all()
    companys = Company.objects.all()

    if request.GET.get('apply') == 'apply':
        print(request.GET.get('studentid'), request.GET.get('postid'))

    return render(request, 'student/home.html', {'posts': posts, 'companys': companys, 'student': request.user.id})


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
    try:
        conn = MongoClient()
        print(conn)
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    # database
    db = conn.rechelp
    db = conn['rechelp']

    # Created or Switched to collection names: my_gfg_collection
    collection = db.post_post
    collection = db['post_post']

    result = collection.update_many(
        {"id": 1},
        {"$set": {"appliedStudents": ['1519bece30060']}, }
    )

    result1 = collection.find({"id": 1}, {"appliedStudents": 1})

    newStudent = '1519bece30038'
    newList = []
    # Print the new record
    cursor = collection.find()
    for record in result1:
        newList = record['appliedStudents']
    print('nl', newList)
    newList.append(newStudent)
    print('nl', newList)
    result = collection.update_many(
        {"id": 1},
        {"$set": {"appliedStudents": newList}, }
    )
