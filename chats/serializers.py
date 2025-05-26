from rest_framework import serializers
from .models import ChatSession,ChatMessage
from django.contrib.auth import get_user_model

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'