from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import BookListSerializer,BookDetailSerializer,BookReportsSerializer,BookReportCommentSerializer,CreateBookReportSerializer,CreateReportCommentSerializer
from .serializers import BookSerializer,ChatSessionBookSerializer
from rest_framework import status
from .models import Book,BookReport,BookReportComment,MbtiRecommend
from .utils.utils import get_data,save_mbti_recommend
from .paginations import StandardResultSetPagination,BookReportResultPagination,CommentResultPagination
from drf_spectacular.utils import extend_schema,OpenApiParameter,OpenApiResponse
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from rest_framework.permissions import IsAdminUser,IsAuthenticatedOrReadOnly,IsAuthenticated
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from django.db.models import Q,Count
from chats.models import ChatSession

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
    request=None,
    responses=BookListSerializer(many=True),
    summary='DB에 저장된 책을 반환하는 API',
    operation_id='book_list_get',
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
    methods=['GET'],
    request=None,
    responses=BookDetailSerializer,
    summary='책을 pk로 상세조회',
    operation_id='book_detail_get',
    description='id : book의 primary key',
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


@extend_schema(
    methods=['POST'],
    request=None,
    responses=inline_serializer(
        name="RecommendBookResponse",
        fields={
            "message": serializers.CharField(),
        }
    ),
    summary='책 추천 / 추천 취소 API',
    operation_id='recommend_book_post',
    description="토글링 방식으로 호출할 것",
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recommend_book(request,book_pk):
    book = get_object_or_404(Book,pk = book_pk)
    if request.method == 'POST':
        if request.user in book.recommend_users.all():
            book.recommend_users.remove(request.user)
            return Response({'message':'도서 추천취소'},status=status.HTTP_200_OK)
        else:
            book.recommend_users.add(request.user)
            return Response({'message':'도서 추천성공'},status=status.HTTP_200_OK)

@extend_schema(
    methods=['GET', 'POST'],
    request={
        'POST': BookReportsSerializer,
        'GET': None,
    },
    responses={
        'GET': BookReportsSerializer(many=True),
        'POST': BookReportsSerializer,
    },
    summary='독후감 리스트, 독후감 저장 API',
    operation_id='book_reports_list_create',
    description="""
### 반환 data의 길이는 30
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
        serializer = CreateBookReportSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(book=book,user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    methods=['GET', 'PUT', 'DELETE'],
    request={
        'PUT': BookReportsSerializer,
        'GET': None,
        'DELETE': None,
    },
    responses={
        'GET': BookReportsSerializer,
        'PUT': BookReportsSerializer,
        'DELETE': inline_serializer(
            name='ReportDeleteResponse',
            fields={'message': serializers.CharField()}
        )
    },
    summary='독후감 상세 조회, 수정, 삭제 API',
    operation_id='report_detail_get_put_delete',
)
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def report_detail(request,book_report_pk,book_pk):
    report = get_object_or_404(BookReport,pk = book_report_pk,book_id = book_pk)
   
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


@extend_schema(
    methods=['POST'],
    request=None,
    responses=inline_serializer(
        name='BookReportLikeResponse',
        fields={
            'message': serializers.CharField()
        }
    ),
    summary='독후감 추천 / 추천 취소 API',
    operation_id='like_book_report_post',
    description="토글 방식으로 좋아요/취소.",
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_book_report(request,book_report_pk,book_pk):
    report = get_object_or_404(BookReport,pk = book_report_pk,book_id=book_pk)
    if request.method == 'POST':
        if request.user in report.like_report_users.all():
            report.like_report_users.remove(request.user)
            return Response({'message':'독후감 좋아요 취소'},status=status.HTTP_200_OK)
        else:
            report.like_report_users.add(request.user)
            return Response({'message':'독후감 좋아요 취소'},status=status.HTTP_200_OK)


@extend_schema(
    methods=['GET', 'POST'],
    request={
        'POST': BookReportCommentSerializer,
        'GET': None,
    },
    responses={
        'GET': OpenApiResponse(
            response=BookReportCommentSerializer(many=True),
            description='댓글 목록 (페이지네이션 포함)'
        ),
        'POST': BookReportCommentSerializer,
    },
    summary='독후감 댓글 목록 조회 및 작성 API',
    description="""
### 페이지네이션 반환 구조
- current_page : 현재 페이지  
- next_page : 다음 페이지  
- previous_page : 이전 페이지  
- count : 전체 댓글 수  
- results : 댓글 리스트 (최대 50개)
""",
    parameters=[
        OpenApiParameter(
            name='page',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='현재 페이지'
        )
    ],
    operation_id='book_report_comments_get_post',
)
@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def book_report_comments(request,book_report_pk,book_pk):
    book_report = get_object_or_404(BookReport,pk=book_report_pk,book_id=book_pk)
    if request.method == 'GET':
        comments = BookReportComment.objects.filter(book_report = book_report)
        paginator = CommentResultPagination()
        result_page = paginator.paginate_queryset(comments,request)
        serializer = BookReportCommentSerializer(result_page,many=True)
        return paginator.get_paginated_response(serializer.data)
    elif request.method == 'POST':
        serializer = CreateReportCommentSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(book_report=book_report,user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@extend_schema(
    methods=['GET', 'PUT', 'DELETE'],
    request={
        'PUT': BookReportCommentSerializer,
        'GET': None,
        'DELETE': None,
    },
    responses={
        'GET': BookReportCommentSerializer,
        'PUT': BookReportCommentSerializer,
        'DELETE': inline_serializer(
            name='CommentDeleteSuccess',
            fields={'message': serializers.CharField()}
        ),
    },
    summary='독후감 댓글 상세 조회, 수정, 삭제 API',
    operation_id='comment_detail_get_put_delete',
)
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
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

@extend_schema(exclude=True)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_mbti_recommend(request):
    if request.method == 'POST':
        save_mbti_recommend()
        return Response({'message':'MBTI 추천 데이터 저장 성공'})
            


@extend_schema(
    summary="추천 도서 리스트 조회",
    description="좋아요 상위 10개 책 + 사용자 채팅 세션 + MBTI 기반 추천 도서(로그인 시)",
    responses={
        200: OpenApiResponse(description="추천 목록 조회 성공", response=BookSerializer(many=True)),
    },
)
@api_view(['GET'])
def recommend_list(request):
    user = request.user

    response_data = {}

    # 좋아요 갯수 가장 많은 순 10개 직렬화 후 응답data에 담음.

    like_top_books = Book.objects.annotate(
        like_count = Count('recommend_users')
    ).order_by('-like_count')[:10]
    response_data['like_top_books'] = BookSerializer(like_top_books,many=True).data

    if request.user.is_authenticated:

        #현재 채팅중인 세션 목록 반환.

        sessions = ChatSession.objects.filter(user=user).select_related('book')[:5]
        response_data['chat_sessions'] = ChatSessionBookSerializer(sessions,many=True).data

        # 유사도 알고리즘으로 저장한 값에서 MBTI에 일치하는 값 내림차순
        mbti = user.mbti
        recommends = MbtiRecommend.objects.filter(mbti=mbti).select_related('book').order_by('-score')
        books = []
        for i in recommends:
            books.append(i.book)

        response_data['recommend_books'] = BookSerializer(books,many=True).data
        return Response(response_data)
    
    return Response(response_data)

@extend_schema(
    summary="도서 검색",
    description="검색 키워드를 포함한 도서 제목을 기준으로 도서를 검색합니다.",
    parameters=[
        OpenApiParameter(
            name="search",
            description="검색할 도서 제목 키워드",
            required=False,
            type=str,
            location=OpenApiParameter.QUERY
        ),
    ],
    responses={
        200: BookListSerializer(many=True),
    },
)
@api_view(['GET'])
def search_book(request):
    if request.method == 'GET':
        keyword = request.query_params.get('search','')
        books = Book.objects.filter(
            Q(title__contains=keyword) | Q(title__contains=keyword)
        )
        serializer = BookListSerializer(books,many=True)
        return Response(serializer.data)