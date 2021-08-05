import uuid
from django.db import models


# Create your models here.

class Register(models.Model):
    Fullname = models.CharField(max_length=30)
    Username = models.CharField(max_length=30)
    Email = models.EmailField()
    Phonenumber = models.IntegerField()
    Password = models.CharField(max_length=30)
    Token = models.CharField(max_length=150)
    Verify = models.BooleanField(default=False)

