from django.forms import ModelForm, Form
from djongo import models
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import HiddenInput
from django.contrib.auth import get_user_model
from company.models import Company
User = get_user_model()


class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(default='', max_length=50)
    lastName = models.CharField(default='', max_length=50)
    enrollmentNumber = models.CharField(default='', max_length=20)
    picture = models.ImageField(
        default='default.png', upload_to='profile_pics', blank=True, null=True)
    wtMarks = models.SmallIntegerField(default='0')
    androidMarks = models.SmallIntegerField(default='0')
    iosMarks = models.SmallIntegerField(default='0')
    javaMarks = models.SmallIntegerField(default='0')
    pythonMarks = models.SmallIntegerField(default='0')
    cpi = models.FloatField(default='0')
    aptitude = models.SmallIntegerField(default='0')
    fieldsOfInterest = models.CharField(default='', max_length=200)
    profileCompleted = models.BooleanField(default=False)

    def __str__(self):
        return self.firstName + " " + self.lastName


class StudentCreationForm(UserCreationForm):
    userType = forms.CharField(required=False, initial="student")
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'required': 'required',
            'placeholder': 'Username',
        }
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'required': 'required',
            'placeholder': 'Password',
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'required': 'required',
            'placeholder': 'Password Confirmation',
        }
    ))

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
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'required': 'required',
            'placeholder': 'Username',
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'required': 'required',
            'placeholder': 'Password',
        }
    ))

    class Meta:
        model = User
        fields = ['username', 'password', 'userType']

    def __init__(self, *args, **kwargs):
        super(StudentLoginForm, self).__init__(*args, **kwargs)
        self.fields['userType'].widget = HiddenInput()


class StudentProfileForm(forms.ModelForm):
    firstName = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    lastName = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    enrollmentNumber = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    cpi = forms.CharField(widget=forms.TextInput(

        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    aptitude = forms.CharField(widget=forms.TextInput(

        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    wtMarks = forms.CharField(widget=forms.TextInput(

        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    androidMarks = forms.CharField(widget=forms.TextInput(

        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    iosMarks = forms.CharField(widget=forms.TextInput(

        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    javaMarks = forms.CharField(widget=forms.TextInput(

        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    pythonMarks = forms.CharField(widget=forms.TextInput(

        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    fieldsOfInterest = forms.CharField(widget=forms.TextInput(

        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))

    class Meta:
        model = Student
        fields = ['firstName', 'lastName',
                  'enrollmentNumber', 'picture', 'cpi', 'aptitude', 'wtMarks', 'androidMarks', 'iosMarks', 'javaMarks', 'pythonMarks', 'fieldsOfInterest', 'user', 'profileCompleted']

    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = HiddenInput()
        self.fields['profileCompleted'].widget = HiddenInput()

    def save(self, commit=True):
        student = super(StudentProfileForm, self).save(commit=False)
        if commit:
            student.save()
        return student


RECRUITED_CHOICES = (
    ('1', 'YES'),
    ('0', 'NO'),

)


class GraduatedStudentForm(forms.Form):

    COMPANY_CHOICES = tuple(
         [(company.name,) * 2 for company in Company.objects.all()])

    RECRUITED_CHOICES = (
        ('1', 'YES'),
        ('0', 'NO'),
    )

    TECHNOLOGY_CHOICES = (
        ('wt', 'wt'),
        ('android', 'android'),
        ('ios', 'ios'),
        ('java', 'java'),
        ('python', 'python'),
    )


    firstName = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    lastName = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    cpi = forms.CharField(widget=forms.TextInput(

        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    aptitude = forms.CharField(widget=forms.TextInput(

        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    wtMarks = forms.CharField(widget=forms.TextInput(

        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    androidMarks = forms.CharField(widget=forms.TextInput(

        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    iosMarks = forms.CharField(widget=forms.TextInput(

        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    javaMarks = forms.CharField(widget=forms.TextInput(

        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    pythonMarks = forms.CharField(widget=forms.TextInput(

        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    recruited = forms.CharField(widget=forms.Select(choices=RECRUITED_CHOICES,
        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    selectedTechnology = forms.CharField(widget=forms.Select(choices=TECHNOLOGY_CHOICES,

        attrs={
            'class': 'form-control',
            'required': 'required'
        }
    ))
    company = forms.CharField(widget=forms.Select(choices=COMPANY_CHOICES,
                                                    attrs={
                                                        'class': 'form-control',
                                                        'required': 'required'
                                                    }
                                                    ))

    def __init__(self, *args, **kwargs):
        super(GraduatedStudentForm, self).__init__(*args, **kwargs)

# class AppliedStudentForm(ModelForm):
#     class Meta:
#         model = Student
#         fields = ['enrollmentNumber']
