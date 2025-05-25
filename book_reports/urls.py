from django.urls import path,include
from . import views

urlpatterns = [
    path('<int:book_report_pk>/', views.report_detail),
    path('<int:book_report_pk>/comments/',include('book_report_comments.urls')),
    path('<int:book_report_pk>/recommend/',views.recommend_book_report)
]
