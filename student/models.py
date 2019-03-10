from django.forms import ModelForm
from djongo import models
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import HiddenInput
from django.contrib.auth import get_user_model
User = get_user_model()
    
class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(default='',max_length=50)
    lastName = models.CharField(default='', max_length=50)
    enrollmentNumber = models.CharField(default='',max_length=20)
    picture = models.ImageField(default='default.png',upload_to='profile_pics')
    wtMarks = models.SmallIntegerField(default='0')
    androidMarks = models.SmallIntegerField(default='0')
    iosMarks = models.SmallIntegerField(default='0')
    javaMarks = models.SmallIntegerField(default='0')
    pythonMarks = models.SmallIntegerField(default='0')
    fieldsOfInterest = models.CharField(default='', max_length=200)
    profileCompleted = models.BooleanField(default=False)

    def __str__(self):
        return self.firstName + " " + self.lastName


class StudentCreationForm(UserCreationForm):
    userType = forms.CharField(required=False, initial="student")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'userType']

    def __init__(self, *args, **kwargs):
        super(StudentCreationForm, self).__init__(*args, **kwargs)
        self.fields['userType'].widget = HiddenInput()

    def save(self, commit=True):
        user = super(StudentCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class StudentLoginForm(AuthenticationForm):
    userType = forms.CharField(required=False, initial="student")

    class Meta:
        model = User
        fields = ['username', 'password', 'userType']

    def __init__(self, *args, **kwargs):
        super(StudentLoginForm, self).__init__(*args, **kwargs)
        self.fields['userType'].widget = HiddenInput()


class SudentProfileForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['firstName', 'lastName',
                  'enrollmentNumber', 'picture', 'wtMarks', 'androidMarks', 'iosMarks', 'javaMarks', 'pythonMarks', 'fieldsOfInterest']

    def __init__(self, *args, **kwargs):
        super(SudentProfileForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        student = super(CompanyProfileForm, self).save(commit=False)
        if commit:
            user.save()
        return student


# class AppliedStudentForm(ModelForm):
#     class Meta:
#         model = Student
#         fields = ['enrollmentNumber']

