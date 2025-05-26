from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.book_list),  # /api/v1/books/
    path('<int:book_pk>/', views.book_detail),  # /api/v1/books/1/
    path('<int:book_pk>/book-reports/', views.book_reports),  # /api/v1/books/1/book-reports/
    path('<int:book_pk>/recommend/',views.recommend_book),
    path('<int:book_pk>/book-reports/<int:book_report_pk>/', views.report_detail),
    path('<int:book_pk>/book-reports/<int:book_report_pk>/like/',views.like_book_report),
    path('<int:book_pk>/book-reports/<int:book_report_pk>/comments/', views.book_report_comments),  # /api/v1/comments/7/
    path('<int:book_pk>/book-reports/<int:book_report_pk>/comments/<int:comments_pk>/', views.comment_detail),  # /api/v1/comments/7/
]
