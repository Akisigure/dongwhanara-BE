from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/book/',include('books.urls')),
    path('accounts/',include('dj_rest_auth.urls')),
    path('accounts/registration/',include('dj_rest_auth.registration.urls'))
]
