from dotenv import load_dotenv
import os
import requests
import xmltodict  # pip install xmltodict

def get_data():
    load_dotenv()
    key = os.getenv('SERVICE_KEY')

    URL = f'http://api.kcisa.kr/openapi/API_LIB_048/request?serviceKey={key}&numOfRows=10000&pageNo=1'
    headers = {
        'Content-Type': 'application/xml',  
        'Accept': 'application/xml'
    }

    res = requests.get(URL, headers=headers)

    xml_data = res.content
    parsed_data = xmltodict.parse(xml_data)

    try:
        items = parsed_data['response']['body']['items']['item']
        return items
    except KeyError:
        print("데이터 파싱 실패. 응답 구조를 확인하세요.")
        return []
