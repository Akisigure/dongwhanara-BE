from django.urls import path,include
from book_reports.views import book_reports
from . import views

urlpatterns = [
    path('', views.book_list),  # /api/v1/books/
    path('<int:book_pk>/', views.book_detail),  # /api/v1/books/1/
    path('<int:book_pk>/book-reports/', book_reports),  # /api/v1/books/1/book-reports/
    path('<int:book_pk>/recommend/',views.recommend_book)
]
