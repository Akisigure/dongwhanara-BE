from django.urls import path,include
from . import views

urlpatterns = [
    path('import-external/',views.get_save_book_data,name='import-external'),
    path('',views.book_list),
    path('<int:book_pk>/',views.book_detail),
    path('<int:book_pk>/book_reports/',include('book_reports.urls')),
]
