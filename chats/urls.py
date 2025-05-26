from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from books.views import get_csrf_token,get_save_book_data
from accounts.views import MyPageView


urlpatterns = [
]
