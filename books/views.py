from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import BookListSerializer,BookDetailSerializer
from .models import Book
from rest_framework import status
from .models import Book
from .utils import get_data
from .paginations import StandardResultSetPagination
from drf_spectacular.utils import extend_schema,OpenApiParameter
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404

# 1회만 호출 Admin만 가능
@extend_schema(exclude=True)
@api_view(['POST'])
@permission_classes([IsAdminUser])
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

    return Response({'message': '저장 성공'},status=status.HTTP_201_CREATED)

# book_list
@extend_schema(
    methods=['GET'],
    responses=BookListSerializer(many=True),
    summary='DB에 저장된 책을 반환하는 API',
    description="""
### 반환 data의 길이는 50
- current_page : 현재 페이지  
- next_page : 다음 페이지  
- previous_page : 이전 페이지  
- count : data의 총 길이
""",
    parameters=[
        OpenApiParameter(
            name='page',
            type=int,
            location=OpenApiParameter.QUERY,
            description='현재 페이지'
        ),
    ]
)
@api_view(['GET'])
def book_list(request):
    if request.method == 'GET':
        book = Book.objects.all()
        paginator = StandardResultSetPagination()
        result_page = paginator.paginate_queryset(book,request)
        serializer = BookListSerializer(result_page,many=True)
        return paginator.get_paginated_response(serializer.data)

@extend_schema(
    summary='책을 pk로 상세조회',
    description='id : book의 primary key',
    responses=BookDetailSerializer,
)
@api_view(['GET'])
def book_detail(request,pk):
    if request.method == 'GET':
        book = get_object_or_404(Book, pk=pk)
        serializer = BookDetailSerializer(book)
        return Response(serializer.data,status=status.HTTP_200_OK)