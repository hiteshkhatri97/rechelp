from djongo import models
from django.contrib.auth.models import User
from student.models import Student
from company.models import Company

class Post(models.Model):

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    techonlogy = models.CharField(default='', max_length=20)
    postDate = models.DateField(auto_now=True)
    postExpiringDate = models.DateField(auto_now=False,blank=True,null=True)

    def __str__(self):
        return self.company + " - " + self.techonlogy
    
