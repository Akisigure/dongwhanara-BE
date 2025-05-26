from dotenv import load_dotenv
import os
import requests
import xmltodict
from books.models import Book,MbtiRecommend
from django.core.exceptions import ObjectDoesNotExist

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


def get_document_simular():
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
# 모델 로딩
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # 데이터 예시
    mbti_profiles = {
        'INTJ': '독립적이고 계획적인 전략가, 목표 지향적',
        'INTP': '호기심 많고 창의적인 아이디어 뱅크',
        'ENTJ': '리더십 강하고 추진력 있는 관리자',
        'ENTP': '토론 즐기고 유연하게 문제 해결하는 혁신가',
        'INFJ': '깊이 있는 통찰력과 가치 중심의 이상주의자',
        'INFP': '감성적이고 개성 강한 조용한 이상주의자',
        'ENFJ': '타인을 이끄는 따뜻한 리더',
        'ENFP': '자유로운 영혼의 열정적인 사람 중심주의자',
        'ISTJ': '신뢰받는 책임감 강한 관리자',
        'ISFJ': '헌신적이고 배려 깊은 조용한 조력자',
        'ESTJ': '조직적이고 체계적인 현실주의 리더',
        'ESFJ': '사교적이며 조화를 중시하는 현실적 배려자',
        'ISTP': '분석적이고 유연한 문제 해결자',
        'ISFP': '예술적 감성의 조용한 자유인',
        'ESTP': '현실적이고 에너지 넘치는 행동가',
        'ESFP': '사교적이며 즉흥적인 분위기 메이커',
    }
    books = list(Book.objects.all().values('title', 'description'))
    print(books)
    book_descriptions = [book['description'] for book in books]
    print(book_descriptions)
    book_vectors = model.encode(book_descriptions)

    mbti_recommendations = {}

    for mbti, profile_text in mbti_profiles.items():
        mbti_vector = model.encode([profile_text])
        similarities = cosine_similarity(mbti_vector, book_vectors)[0]

        top_books = sorted(zip(books, similarities), key=lambda x: x[1], reverse=True)[:5]  # 상위 5권 추천
        mbti_recommendations[mbti] = [
            {"title": b['title'], "score": round(score, 3)} for b, score in top_books
        ]

    return mbti_recommendations


def save_mbti_recommend():
    recommend = get_document_simular()

    #중복되지 않게 기존에 측정한 정확도는 삭제
    MbtiRecommend.objects.all().delete()

    for mbti, books in recommend.items():
        for book_info in books:
            title = book_info['title']
            score = book_info['score']
            try:
                book = Book.objects.get(title=title)
                mbti_recommend = MbtiRecommend()
                mbti_recommend.mbti = mbti
                mbti_recommend.book = book
                mbti_recommend.score = score
                mbti_recommend.save()
            except Book.DoesNotExist:
                continue


