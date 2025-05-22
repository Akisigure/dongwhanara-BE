from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BookListSerializer
from .models import Book
from rest_framework import status

from dotenv import load_dotenv
import os
import requests
from .models import Book

@api_view(['GET'])
def get_save_book_data(request) :
    load_dotenv()
    key = os.getenv('ALADIN_KEY')
    start_cnt = 1
    category_id = 48810
    total_result = 0
    while True:
        req = requests.get(f'http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey={key}&QueryType=ItemNewAll&MaxResults=50&start={start_cnt}&SearchTarget=Book&CategoryId={category_id}&output=js&Version=20131101')
        data = req.json()
        start_idx = data['startIndex']
        api_cnt = data['totalResults']
        page = data['itemsPerPage']

        if total_result == 0:
            total_result = api_cnt
        print(api_cnt)
        print(start_idx)

        total_result -= page

        start_cnt += 1

        for i in range(len(data['item'])):
            book_data = data['item'][i]
            book = Book()
            book.title = book_data['title']
            book.adult = book_data['adult']
            book.cover = book_data['cover']
            book.author = book_data['author']
            book.description = book_data['description']
            book.category_id = book_data['categoryId']
            book.price_standard = book_data['priceStandard']
            book.link = book_data['link']
            book.publisher = book_data['publisher']
            book.save()

        if total_result <= 0:
            break
    return Response({'message': 'Books saved successfully!'},status=status.HTTP_201_CREATED)
