from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    pass
    uuid = models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    gender = models.CharField(max_length=15)
    mbti = models.CharField(max_length=4)
    content = models.TextField(blank=True)
    
