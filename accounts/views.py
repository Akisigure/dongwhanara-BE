from dj_rest_auth.views import UserDetailsView
from .serializers import MyPageSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.urls import path
from django.http import JsonResponse


class MyPageView(UserDetailsView):
    serializer_class = MyPageSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user

class AdminOnlySpectacularAPIView(UserPassesTestMixin, SpectacularAPIView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        return JsonResponse(
            {'detail': '관리자만 접근 가능합니다.'},
            status=403
        )

class AdminOnlySpectacularSwaggerView(UserPassesTestMixin, SpectacularSwaggerView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        return JsonResponse(
            {'detail': '관리자만 접근 가능합니다.'},
            status=403
        )

class AdminOnlySpectacularRedocView(UserPassesTestMixin, SpectacularRedocView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        return JsonResponse(
            {'detail': '관리자만 접근 가능합니다.'},
            status=403
        )