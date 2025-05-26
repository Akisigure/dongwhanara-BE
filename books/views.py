from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import BookListSerializer,BookDetailSerializer,BookReportsSerializer,BookReportCommentSerializer
from rest_framework import status
from .models import Book,BookReport,BookReportComment
from .utils import get_data
from .paginations import StandardResultSetPagination,BookReportResultPagination,CommentResultPagination
from drf_spectacular.utils import extend_schema,OpenApiParameter
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from rest_framework.permissions import IsAdminUser,IsAuthenticatedOrReadOnly


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
def book_detail(request,book_pk):
    if request.method == 'GET':
        book = get_object_or_404(Book, pk=book_pk)
        serializer = BookDetailSerializer(book)
        return Response(serializer.data,status=status.HTTP_200_OK)


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'message': 'CSRF cookie set'})


@api_view(['POST'])
def recommend_book(request,book_pk):
    book = get_object_or_404(Book,pk = book_pk)
    if request.method == 'POST':
        if request.user in book.recommend_users.all():
            book.recommend_users.remove(request.user)
            return Response({'message':'도서 추천취소'},status=status.HTTP_200_OK)
        else:
            book.recommend_users.add(request.user)
            return Response({'message':'도서 추천성공'},status=status.HTTP_200_OK)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def book_reports(request,book_pk):
    book = get_object_or_404(Book,pk=book_pk)

    if request.method == 'GET':
        reports = BookReport.objects.filter(book=book)
        paginator = BookReportResultPagination()
        result_page = paginator.paginate_queryset(reports,request)
        serializer = BookReportsSerializer(result_page,many=True)
        return paginator.get_paginated_response(serializer.data)
    
    if request.method == 'POST':
        serializer = BookReportsSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(book=book,user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def report_detail(request,report_pk,book_pk):
    report = get_object_or_404(BookReport,pk = report_pk,book_id = book_pk)
   
    if request.method == 'GET':
        serializer = BookReportsSerializer(report)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        if report.user == request.user:
            report.delete()
            return Response({'message':'삭제 성공.'},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message':'권한이 없습니다.'},status=status.HTTP_403_FORBIDDEN)
    
    elif request.method == 'PUT':
        if report.user == request.user:
            serializer = BookReportsSerializer(report, data = request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'message':'권한이 없습니다.'},status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
def like_book_report(request,book_report_pk,book_pk):
    report = get_object_or_404(BookReport,pk = book_report_pk,book_id=book_pk)
    if request.method == 'POST':
        if request.user in report.like_report_users.all():
            report.like_report_users.remove(request.user)
            return Response({'message':'독후감 좋아요 취소'},status=status.HTTP_200_OK)
        else:
            report.like_report_users.add(request.user)
            return Response({'message':'독후감 좋아요 취소'},status=status.HTTP_200_OK)

@api_view(['GET','POST'])
def book_report_comments(request,book_report_pk,book_pk):
    book_report = get_object_or_404(BookReport,pk=book_report_pk,book_id=book_pk)
    if request.method == 'GET':
        comments = BookReportComment.objects.filter(book_report = book_report)
        paginator = CommentResultPagination()
        result_page = paginator.paginate_queryset(comments,request)
        serializer = BookReportCommentSerializer(result_page,many=True)
        return paginator.get_paginated_response(serializer.data)
    elif request.method == 'POST':
        serializer = BookReportCommentSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(book_report=book_report,user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view(['GET','PUT','DELETE'])
def comment_detail(request,comment_pk,book_report_pk,book_pk):

    comment = get_object_or_404(BookReportComment,pk=comment_pk,book_report_id=book_report_pk,book_id=book_pk)
    
    if request.method == 'GET':
        serializer = BookReportCommentSerializer(comment)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        if comment.user == request.user:
            serializer = BookReportCommentSerializer(comment,data = request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    elif request.method == 'DELETE':
        if comment.user == request.user:
            comment.delete()
            return Response({'message':'삭제성공'},status=status.HTTP_204_NO_CONTENT)
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)