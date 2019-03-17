from django.contrib.auth.models import AbstractUser
from django.db import models


class RecHelpeUser(AbstractUser):
    userType = models.CharField(blank=True, max_length=8)


