from django.urls import path
from . import views

urlpatterns = [
    path('test/',views.get_save_book_data),
    path('list/',views.book_list),
]
