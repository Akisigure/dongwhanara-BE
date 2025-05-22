from dotenv import load_dotenv
import os
import requests
from .models import Book

def get_save_book_data() :
    load_dotenv()
    key = os.getenv('ALADIN_KEY')
    start_cnt = 1
    category_id = 48810
    total_result = 0
    call_cnt = 50
    while True:
        req = requests.get(f'http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey={key}&QueryType=ItemNewAll&MaxResults={call_cnt}&start={start_cnt}&SearchTarget=Book&CategoryId={category_id}&output=js&Version=20131101')
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

        if total_result <= 0:
            break

        for i in range(len(data['item'])):
            print(data['item'][i]['title']) 
            book = Book()
            book.title = data['item'][i]['title']
            book.save()



