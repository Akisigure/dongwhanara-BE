from django.db import models
from books.models import Book
from django.contrib.auth import get_user_model

# Create your models here.
class Prompt(models.Model):
    book = models.OneToOneField(Book,on_delete=models.CASCADE)
    prompt_description = models.TextField(null=True,blank=True)
    name = models.CharField(max_length=50,null=True,blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

class ChatSession(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]
    session = models.ForeignKey(ChatSession,related_name='messages',on_delete=models.CASCADE)
    message = models.TextField(null=True)
    sender_role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

