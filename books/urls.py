from django.urls import path
from . import views

urlpatterns = [
    path('import-external/',views.get_save_book_data,name='import-external'),
    path('',views.book_list),
    path('<int:pk>/',views.book_detail)
]
