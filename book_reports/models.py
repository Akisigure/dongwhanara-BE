from django.db import models
from books.models import Book
from django.contrib.auth import get_user_model

# Create your models here.
class BookReport(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    report_title = models.CharField(max_length=50)
    report_content = models.TextField()
    report_created_at = models.DateTimeField(auto_now_add=True)
    report_updated_at = models.DateTimeField(auto_now=True)
    image = models.URLField(blank=True)
    