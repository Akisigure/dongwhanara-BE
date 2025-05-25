from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model

class SignUpSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    gender = serializers.CharField(required=True)
    mbti = serializers.CharField()
    content = serializers.CharField()
    
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name')
        data['last_name'] = self.validated_data.get('last_name')
        data['gender'] = self.validated_data.get('gender')
        data['mbti'] = self.validated_data.get('mbti')
        data['content'] = self.validated_data.get('content')

        return data
    
    def save(self,request):
        user = super().save(request)
        user.first_name = self.validated_data.get('first_name')
        user.last_name = self.validated_data.get('last_name')
        user.gender = self.validated_data.get('gender')
        user.mbti = self.validated_data.get('mbti')
        user.content = self.validated_data.get('content')
        user.save()
        return user
    
class MyPageSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        model = get_user_model()
        fields = UserDetailsSerializer.Meta.fields + (
            'uuid','gender','mbti','content',
        )
