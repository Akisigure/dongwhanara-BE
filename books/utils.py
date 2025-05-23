from dotenv import load_dotenv
import os
import requests

def get_data() :
    load_dotenv()
    key = os.getenv('SERVICE_KEY')
    URL = f'http://api.kcisa.kr/openapi/API_LIB_048/request?serviceKey={key}&numOfRows=10000&pageNo=1'
    headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}
    res = requests.get(URL,headers=headers)

    #data
    data = res.json()['response']['body']['items']['item']

    return data