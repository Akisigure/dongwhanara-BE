from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from books.views import get_csrf_token
from accounts.views import MyPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('dj_rest_auth.urls')),
    path('accounts/registration/',include('dj_rest_auth.registration.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'),name='redoc'),

    path('api/v1/books/', include('books.urls')),
    path('api/v1/csrf/', get_csrf_token),
    path('accounts/my-page/',MyPageView.as_view(),name='my-page')
]
