from django.db import models
from book_reports.models import BookReport
from django.contrib.auth import get_user_model

# Create your models here.
class BookReportComment(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    book_report = models.ForeignKey(BookReport,on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    