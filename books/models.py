from django.db import models
from django.contrib.auth import get_user_model

class Book(models.Model):
    title = models.CharField(max_length=80)
    image_object = models.URLField()
    author = models.CharField(max_length=20,blank=True,null=True,default='미상')
    description = models.TextField(blank=True,null=True)
    url = models.URLField()
    view_count = models.IntegerField()
    recommend_users = models.ManyToManyField(
        get_user_model(),
        related_name='recommend_reports',
        blank=True,
    )

class BookReport(models.Model):
    book = models.ForeignKey(Book,related_name='book_reports',on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    report_title = models.CharField(max_length=50)
    report_content = models.TextField()
    report_created_at = models.DateTimeField(auto_now_add=True)
    report_updated_at = models.DateTimeField(auto_now=True)
    
    like_report_users = models.ManyToManyField(
        get_user_model(),
        related_name='like_reports',
        blank=True,
    )

class BookReportComment(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    book_report = models.ForeignKey(BookReport,related_name='report_comments',on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MbtiRecommend(models.Model):
    mbti = models.CharField(max_length=4)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    score = models.FloatField()

    class Meta:
        unique_together = ('mbti', 'book')