from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('test/',views.get_save_book_data),
    path('list/',views.book_list),
]
