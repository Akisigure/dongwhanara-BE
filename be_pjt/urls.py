from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from books.views import get_csrf_token,get_save_book_data
from accounts.views import MyPageView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('dj_rest_auth.urls')),
    path('accounts/registration/',include('dj_rest_auth.registration.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'),name='redoc'),

    path('api/v1/books/', include('books.urls')),                # 책 관련
    path('api/v1/book-reports/', include('book_reports.urls')),  # 독후감 관련
    path('api/v1/comments/', include('book_report_comments.urls')),  # 댓글 관련
    path('api/v1/csrf/', get_csrf_token),
    path('accounts/my-page/',MyPageView.as_view(),name='my-page'),
    path('api/v1/test/',get_save_book_data)
]
