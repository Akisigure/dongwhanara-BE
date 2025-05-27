from rest_framework import serializers
from .models import Book,BookReport,BookReportComment
from django.contrib.auth import get_user_model
from chats.models import ChatSession
from chats.serializers import PromptSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =('last_name','first_name','username')

class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookReportCommentSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = BookReportComment
        fields = '__all__'
        read_only_fields = ('book_report',)

class BookReportsSerializer(serializers.ModelSerializer):

    class CustomBookDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Book
            fields = '__all__'

    user = UserSerializer(read_only=True)
    report_comments = BookReportCommentSerializer(many=True, read_only=True)

    class Meta:
        model = BookReport
        fields = '__all__'

class CreateBookReportSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    report_comments = BookReportCommentSerializer(many=True,read_only=True)
    class Meta:
        model = BookReport
        fields = '__all__'
        read_only_fields = ('book',)

class CreateReportCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = BookReportComment
        fields = '__all__'
        read_only_fields = ('book_report',)


class BookDetailSerializer(serializers.ModelSerializer):
    class CustomBookReportSerializer(serializers.ModelSerializer):
        class Meta:
            model = BookReport
            fields = '__all__'
        user = UserSerializer(read_only=True)
        
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
    prompt = PromptSerializer(read_only=True)
    class Meta:
        model = ChatSession
        fields = ['book', 'has_message']

    def get_has_message(self, obj):
        return obj.messages.exists()