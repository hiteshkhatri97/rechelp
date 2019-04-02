from djongo import models
from django.contrib.auth.models import User
from student.models import Student
from company.models import Company
from django.forms import ModelForm
from django import forms
from django.forms.widgets import HiddenInput

TECHNOLOGY_CHOICES = (
    ('wt', 'wt'),
    ('android', 'android'),
    ('ios', 'ios'),
    ('java', 'java'),
    ('python', 'python'),

)


class Post(models.Model):

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    postDate = models.DateField(auto_now=True)
    postExpiringDate = models.DateField(auto_now=False, blank=True, null=True)
    postTechnology = models.CharField(
        max_length=10, choices=TECHNOLOGY_CHOICES, default='wt')

    def __str__(self):
        return self.company.name + " - " + self.postTechnology


class DateInput(forms.DateInput):
    input_type = 'date'


class addPostForm(ModelForm):
    postExpiringDate = forms.DateField(
        widget=forms.DateInput(
            attrs={
            'type': 'date',
            'class':'form-control'
            }
            ))
    postTechnology = forms.CharField(
        widget=forms.Select(choices=TECHNOLOGY_CHOICES,
            attrs={
            'class':'form-control'
            }
            ))

    class Meta:
        model = Post
        fields = ['postTechnology', 'company', 'postExpiringDate']

    def __init__(self, *args, **kwargs):
        super(addPostForm, self).__init__(*args, **kwargs)
        self.fields['company'].widget = HiddenInput()
        # widgets = {
        #     'postExpiringDate': DateInput(),
        # }
