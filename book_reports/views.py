from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from.serializers import BookReportsSerializer
from rest_framework import status
from drf_spectacular.utils import extend_schema,OpenApiParameter
from rest_framework.permissions import IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import BookReport
from books.models import Book

@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def book_reports(request,book_pk):
    book = get_object_or_404(Book,pk=book_pk)

    if request.method == 'GET':
        reports = BookReport.objects.filter(book=book)
        serializer = BookReportsSerializer(reports, many=True)
        return Response(serializer.data)
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



