from django.urls import path,include
from book_report_comments.views import book_report_comments
from . import views

urlpatterns = [
    path('<int:book_report_pk>/', views.report_detail),  # /api/v1/book-reports/3/
    path('<int:book_report_pk>/comments/',include('book_report_comments.urls'))
]
