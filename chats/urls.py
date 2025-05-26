from django.urls import path,include
from . import views

urlpatterns = [
    path('<int:book_pk>/',views.create_prompt)
]
