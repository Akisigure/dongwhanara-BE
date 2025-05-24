from rest_framework import serializers
from .models import BookReport
from books.models import Book
from django.contrib.auth import get_user_model

class BookReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReport
        fields = '__all__'
        read_only_fields = ('book','user',)

class CsrfmiddlewaretokenSerializer(serializers.Serializer):
    csrfmiddlewaretoken = serializers.CharField(max_length=64)