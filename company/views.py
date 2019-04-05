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
def editPost(request):
    print(request)
    print("editreach")
    postid=Post.objects.filter(id=request.GET.get('postid')).first()
    print("postidgot")
    print(postid)
    return addPost(request,postid)

@login_required(login_url="company:login")
def home(request):

    currentCompanyPosts = Post.objects.filter(
        company=getCurrentCompany(request))
    postDatesSet = set([post.postDate for post in currentCompanyPosts])

    if request.GET.get('editpost')=='edit post':
        return editPost(request)

    if request.GET.get('delete') == 'delete':
        deletePost(request.GET.get('postid'))
        return redirect('company:home')

    if request.GET.get('appliedstudents') == 'applied students':
        return appliedStudents(request)

    if request.GET.get('viewprofile') == 'viewprofile':
        return viewOutsideProfile(request, int(request.GET.get('studentid')))

    if request.GET.get('select') == 'select':
        studentid = request.GET.get('studentid')
        postid = request.GET.get('postid')
        selectStudent(postid, studentid)
        return appliedStudents(request)

    return render(request, 'company/home.html', {'posts': enumerate(currentCompanyPosts), 'postDatesSet': postDatesSet})


@login_required(login_url="company:login")
def addPost(request,instance=None):
    print("addpostreach")
    print(instance)
    company = getCurrentCompany(request)
    if company.profileCompleted == False:
        return redirect('company:editprofile')
    if instance is None:
        formInitialData = {'company': company}
        form = addPostForm(initial=formInitialData)
    else:
        formInitialData = {'company': company}
        form = addPostForm(initial=formInitialData,instance=instance)

    if request.method == 'POST':
        form = addPostForm(
            request.POST,instance=instance)
        if form.is_valid():
            newPost = form.save()

            collection = connectDatabase()

            result = collection.update(
                {'id': int(newPost.id)}, {'$set': {'appliedStudents': [], 'selectedStudents': []}})

            return redirect('company:home')
    elif not(instance is None):
        return render(request, 'company/editpost.html', {'form': form})
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
    post = Post.objects.filter(id=postid)

    applied_students = getAppliedStudents(postid)
    selected_students = getSelectedStudents(postid)
    return render(request, 'company/appliedstudents.html', {'appliedStudents': applied_students, 'postid': postid, 'selectedStudents': selected_students})


def viewOutsideProfile(request, studentid):
    student = Student.objects.filter(id=studentid)
    details = [(field.name, getattr(student[0], field.name))
               for field in Student._meta.get_fields() if field.name == 'enrollmentNumber' or field.name == 'fieldsOfInterest']
    marks = [(field.name.replace("Marks", ""), getattr(student[0], field.name)) for field in Student._meta.get_fields(
    ) if 'Marks' in field.name or field.name == 'cpi' or field.name == 'aptitude']
    return render(request, 'company/outsideprofile.html', {'marks': marks, 'details': details, 'student': student[0]})


def selectStudent(postid, studentid):
    collection = connectDatabase()
    cursor = list(collection.find({"id": int(postid)}, {
                  "selectedStudents": 1, '_id': 0}))[0]['selectedStudents']

    if int(studentid) not in cursor:
        cursor.append(int(studentid))

    result = collection.update(
        {'id': int(postid)}, {'$set': {'selectedStudents': cursor}})


def getAppliedStudents(postid):
    collection = connectDatabase()
    result = list(collection.find({'id': int(postid)}, {
        'appliedStudents': 1, '_id': 0}))[0]['appliedStudents']

    applied_students = []

    if len(result) > 0:
        for id in result:
            applied_students = [Student.objects.filter(
                id=int(id))[0] for id in result]

    post_technology = Post.objects.filter(id=int(postid))[0].postTechnology
    print(post_technology)
    
    applied_students_marks = []

    for student in applied_students:
        current_students_marks_total = 0
        for field in Student._meta.get_fields():            
            # normalizing the marks out of 100 and multiplying with weights. if current marks are posted technologythen weight = 0.7 else 0.2
            if 'Marks' in field.name:
                current_field = field.name.replace("Marks", "")
                if current_field == post_technology:
                    current_students_marks_total += (getattr(student, field.name) * 100 / 70) * 0.7
                else:
                    current_students_marks_total += (getattr(student, field.name) * 100 / 70) * 0.2
            elif field.name == 'cpi':
                current_students_marks_total += (getattr(student, field.name) * 100 / 10) * 0.2
            elif field.name == 'aptitude':
                current_students_marks_total += getattr(student, field.name) * 0.2
        # applying multiple linear regression formula : y = b1x1 + b2x2 + ... where x are marks, b are weights
        applied_students_marks.append(current_students_marks_total)

    # associatingstudents with their ML score
    appliedStudents = list(zip(applied_students, applied_students_marks))

    # sorting the applied students in descending order
    sorted_applied_students = [student[0] for student in sorted(
        appliedStudents, key=lambda appliedStudents: appliedStudents[1], reverse = True)]

    return sorted_applied_students


def getSelectedStudents(postid):
    collection = connectDatabase()
    result = list(collection.find({'id': int(postid)}, {
        'selectedStudents': 1, '_id': 0}))[0]['selectedStudents']
    selected_students = []
    if len(result) > 0:
        for id in result:
            selected_students = [Student.objects.filter(
                id=int(id))[0] for id in result]
    return selected_students
