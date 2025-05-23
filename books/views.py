from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BookListSerializer
from .models import Book
from rest_framework import status
from .models import Book
from .utils import get_data
from .paginations import StandardResultSetPagination

@api_view(['GET'])
def get_save_book_data(request) :
    data = get_data()
    print(data)
    for i in range(len(data)):
        book = Book()
        book.title = data[i].get('title')
        book.description = data[i].get('description')
        book.author = data[i].get('author') or '미상'
        book.url = data[i].get('url')
        book.image_object = data[i].get('image_object')
        book.view_count = data[i].get('view_count')
        book.save()

    return Response({'message': 'Books saved successfully!'},status=status.HTTP_201_CREATED)

@api_view(['GET'])
def book_list(request):
    book = Book.objects.all()
    paginator = StandardResultSetPagination()
    result_page = paginator.paginate_queryset(book,request)
    serializer = BookListSerializer(result_page,many=True)
    return paginator.get_paginated_response(serializer.data)