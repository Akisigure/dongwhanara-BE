from django.urls import path,include
from . import views

urlpatterns = [
    path('<int:book_pk>/session/',views.start_session),
    path('<int:book_pk>/session/<int:session_pk>/messages/',views.send_message)
]
