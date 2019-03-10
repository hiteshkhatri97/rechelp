from django.contrib.auth.models import AbstractUser
from django.db import models


class RecHelpeUser(AbstractUser):
    userType = models.CharField(blank=True, max_length=8)


# class RecHelpeUserForm(UserCreationForm):
#     userTypeField = forms.CharField(required=False, default='')

#     class Meta:
#         model = RecHelpeUserForm
#         fields = ('username', 'password1', 'password2', 'userTypeField')

#     def save(self, commit=True):
#         user = super(RecHelpeUserForm, self).save(commit=False)
#         if commit:
#             user.save()
#         return user
