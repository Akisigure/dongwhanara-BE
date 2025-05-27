from rest_framework import serializers
from .models import ChatSession,ChatMessage,Prompt
from django.contrib.auth import get_user_model

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'

class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = '__all__'

class CustomSessionSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    prompt_name = serializers.SerializerMethodField()
    prompt_image = serializers.SerializerMethodField()
    messages = ChatSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ('id', 'book', 'book_title', 'prompt_name', 'prompt_image', 'started_at', 'messages',)

    def get_prompt_name(self, obj):
        prompt = getattr(obj.book, 'prompt', None)
        return prompt.name if prompt else None

    def get_prompt_image(self, obj):
        prompt = getattr(obj.book, 'prompt', None)
        if prompt and prompt.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(prompt.image.url)
            return prompt.image.url
        return None

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('id', 'message', 'sender_role', 'created_at', 'session',)