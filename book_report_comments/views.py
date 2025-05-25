from rest_framework.decorators import api_view
from .serializers import BookReportCommentSerializer
from .models import BookReportComment
from .paginations import CommentResultPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from book_reports.models import BookReport
from rest_framework import status

# Create your views here.
@api_view(['GET','POST'])
def book_report_comments(request,book_report_pk):
    book_report = get_object_or_404(BookReport,pk=book_report_pk)
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
def comment_detail(request,comment_pk,book_report_pk):

    comment = get_object_or_404(BookReportComment,pk=comment_pk,book_report_id=book_report_pk)
    
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
