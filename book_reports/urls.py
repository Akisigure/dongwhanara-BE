from django.urls import path
from . import views

urlpatterns = [
    path('',views.book_reports),
    path('<int:report_pk>/',views.report_detail),
]
