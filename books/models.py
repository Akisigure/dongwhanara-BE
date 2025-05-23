from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=80)
    image_object = models.URLField()
    author = models.CharField(max_length=20,blank=True,null=True,default='미상')
    description = models.TextField(blank=True,null=True)
    url = models.URLField()
    view_count = models.IntegerField()