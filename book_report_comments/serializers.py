from rest_framework import serializers
from .models import BookReportComment

class BookReportCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReportComment
        fields = '__all__'
        read_only_fields = ('book_report','user',)
        