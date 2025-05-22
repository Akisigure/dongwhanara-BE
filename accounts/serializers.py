from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

class SignUpSerializer(RegisterSerializer):
    gender = serializers.CharField(required=True)
    mbti = serializers.CharField()
    content = serializers.CharField()
    
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['gender'] = self.validated_data.get('gender')
        data['mbti'] = self.validated_data.get('mbti')
        data['content'] = self.validated_data.get('content')
        return data
    
    def save(self,request):
        user = super().save(request)
        user.gender = self.validated_data.get('gender')
        user.mbti = self.validated_data.get('mbti')
        user.content = self.validated_data.get('content')
        user.save()
        return user