from rest_framework import serializers
from .models import BookReport
from books.models import Book
from django.contrib.auth import get_user_model

class BookReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReport
        fields = '__all__'
        read_only_fields = ('book','user',)

# GET 요청 생길때까지만 유지
class CsrfmiddlewaretokenSerializer(serializers.Serializer):
    csrfmiddlewaretoken = serializers.CharField(max_length=64)

# class ReportRecommendSerializer(serializers.ModelSerializer):
#     recommend_users = serializers.PrimaryKeyRelatedField(
#         many=True,read_only=True
#     )
#     recommend_count = serializers.SerializerMethodField()
#     class Meta:
#         model = BookReport
#         fields = '__all__'
    
#     def get_recommend_count(self,obj):
#         return obj.recommend_users.count()