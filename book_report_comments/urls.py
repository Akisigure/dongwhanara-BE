from django.urls import path,include
from. import views

urlpatterns = [
    path('', views.book_report_comments),  # /api/v1/comments/7/
    path('<int:comment_pk>/', views.comment_detail),  # /api/v1/comments/7/
]
