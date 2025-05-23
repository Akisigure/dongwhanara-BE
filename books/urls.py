from django.urls import path
from . import views

urlpatterns = [
    path('import-external/',views.get_save_book_data),
    path('/',views.book_list),
    
]
