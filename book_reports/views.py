from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from.serializers import BookReportsSerializer
from rest_framework import status
from drf_spectacular.utils import extend_schema,OpenApiParameter
from rest_framework.permissions import IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import BookReport
from books.models import Book
from .paginations import BookReportResultPagination

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
def recommend_book_report(request,book_report_pk):
    report = get_object_or_404(BookReport,pk = book_report_pk)
    if request.method == 'POST':
        if request.user in report.recommend_users.all():
            report.recommend_users.remove(request.user)
            return Response({'message':'추천취소'},status=status.HTTP_200_OK)
        else:
            report.recommend_users.add(request.user)
            return Response({'message':'추천성공'},status=status.HTTP_200_OK)
        