from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass
    gender = models.CharField(max_length=15)
    mbti = models.CharField(max_length=4)
    content = models.TextField(null=True)