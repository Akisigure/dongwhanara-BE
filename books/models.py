from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=80)
    cover = models.URLField()
    author = models.CharField(max_length=20)
    description = models.TextField()
    adult = models.BooleanField()
    category_id = models.IntegerField()
    price_standard = models.IntegerField()
    link = models.URLField()
    publisher = models.CharField(max_length=50)