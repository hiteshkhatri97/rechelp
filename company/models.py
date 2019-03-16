from django.forms import ModelForm
from djongo import models
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import HiddenInput
from django.contrib.auth import get_user_model
User = get_user_model()


class Company(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(default='', max_length=200)
    email = models.EmailField(default='')
    phone = models.BigIntegerField(default='0')
    address = models.TextField(default='')
    profileCompleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CompanyCreationForm(UserCreationForm):
    userType = forms.CharField(required=False, initial="company")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'userType']

    def __init__(self, *args, **kwargs):
        super(CompanyCreationForm, self).__init__(*args, **kwargs)
        self.fields['userType'].widget = HiddenInput()

    def save(self, commit=True):
        user = super(CompanyCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class CompanyLoginForm(AuthenticationForm):
    userType = forms.CharField(required=False, initial="company")

    class Meta:
        model = User
        fields = ['username', 'password', 'userType']

    def __init__(self, *args, **kwargs):
        super(CompanyLoginForm, self).__init__(*args, **kwargs)
        self.fields['userType'].widget = HiddenInput()


class CompanyProfileForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['name', 'email', 'phone',
                  'address', 'user', 'profileCompleted']

    def __init__(self, *args, **kwargs):
        super(CompanyProfileForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = HiddenInput()
        self.fields['profileCompleted'].widget = HiddenInput()
