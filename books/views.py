from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BookListSerializer
from .models import Book
from rest_framework import status
from dotenv import load_dotenv
import os
import requests
from .models import Book
from .utils import get_data

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
