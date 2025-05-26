from django.db import models
from books.models import Book

# Create your models here.
class Promprt(models.Model):
    book = models.OneToOneField(Book,on_delete=models.CASCADE)
    prompt_description = models.TextField(null=True,blank=True)
    name = models.CharField(max_length=50,null=True,blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
