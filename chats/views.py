from django.shortcuts import render
from rest_framework.decorators import api_view
from .utils import prompt
from rest_framework.response import Response
from rest_framework import status
from .models import Promprt
from django.shortcuts import get_object_or_404
from books.models import Book

@api_view(['POST'])
def create_prompt(request,book_pk):
    if request.method == 'POST':
        book = get_object_or_404(Book,pk = book_pk)
        
        if Promprt.objects.filter(book=book).exists():
            return Response({'message':'이미 프롬프트가 존재합니다'},status=status.HTTP_400_BAD_REQUEST)
        message = prompt.get_prompt(book.title,book.description)
        name = message[0]
        prompt_description = message[1]
        url = prompt.get_cover_img(name,prompt_description)
        print(url)
        prompt_data = Promprt()
        prompt_data.name = name
        prompt_data.prompt_description = prompt_description
        prompt_data.image = url
        prompt_data.book = book

        prompt_data.save()

    return Response({'message':'저장 성공'},status=status.HTTP_200_OK)