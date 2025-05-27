from rest_framework import serializers
from .models import Book,BookReport,BookReportComment
from django.contrib.auth import get_user_model
from chats.models import ChatSession

class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookReportCommentSerializer(serializers.ModelSerializer):
    class CustomUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('last_name', 'first_name', 'username')
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = BookReportComment
        fields = '__all__'
        read_only_fields = ('book_report',)

class BookReportsSerializer(serializers.ModelSerializer):
    class CustomUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('last_name', 'first_name', 'username')

    class CustomBookDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Book
            fields = '__all__'

    user = CustomUserSerializer(read_only=True)
    # book = CustomBookDetailSerializer(read_only=True)
    report_comments = BookReportCommentSerializer(many=True, read_only=True)

    class Meta:
        model = BookReport
        fields = '__all__'

class CreateBookReportSerializer(serializers.ModelSerializer):
    class CustomUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('last_name', 'first_name', 'username')
    user = CustomUserSerializer(read_only=True)
    report_comments = BookReportCommentSerializer(many=True,read_only=True)
    class Meta:
        model = BookReport
        fields = '__all__'
        read_only_fields = ('book',)

class CreateReportCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReportComment
        fields = '__all__'
        read_only_fields = ('book_report','user',)


class BookDetailSerializer(serializers.ModelSerializer):
    class CustomBookReportSerializer(serializers.ModelSerializer):
        class Meta:
            model = BookReport
            fields = '__all__'
        class CustomUserSerializer(serializers.ModelSerializer):
            class Meta:
                model = get_user_model()
                fields = ('last_name','first_name','username',)
        user = CustomUserSerializer(read_only=True)
        
    book_reports = CustomBookReportSerializer(many=True,read_only=True)
    class Meta:
        model = Book
        fields = '__all__'

class CsrfmiddlewaretokenSerializer(serializers.Serializer):
    csrfmiddlewaretoken = serializers.CharField(max_length=64)

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class ChatSessionBookSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    has_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = ['book', 'has_message']

    def get_has_message(self, obj):
        return obj.messages.exists()