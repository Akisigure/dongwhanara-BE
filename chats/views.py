from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from .utils.prompt import create_prompt,response_chat
from rest_framework.response import Response
from rest_framework import status
from .models import Prompt,ChatSession,ChatMessage
from django.shortcuts import get_object_or_404
from books.models import Book
from rest_framework.permissions import IsAuthenticated
from .serializers import SessionSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_session(request,book_pk):
    book = get_object_or_404(Book,pk = book_pk)
    prompt = Prompt.objects.filter(book=book).first()
    if not prompt:
        prompt = create_prompt(book)    
    session = ChatSession.objects.filter(user = request.user, book=book).first()
    if not session:
        session = ChatSession()
        session.user = request.user
        session.book = book
        session.save()
    
    serializer = SessionSerializer(session)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request,session_pk,book_pk):
    session = get_object_or_404(ChatSession,pk = session_pk,book__pk = book_pk, user=request.user)
    user_message = request.data.get('message')
    if not user_message:
        return Response({'error':'메세지를 입력해주세요.'},status=status.HTTP_400_BAD_REQUEST)

    user_chat = ChatMessage()
    user_chat.session = session
    user_chat.sender_role = 'user'
    user_chat.message = user_message

    user_chat.save()

    messages = session.messages.all().order_by('created_at')

    gpt_messages = []

    prompt = session.book.prompt
    if prompt:
        gpt_messages.append({'role':'system','content':prompt.prompt_description})
    
    for msg in messages:
        if msg.message and msg.message.strip():
            gpt_messages.append({
            'role': msg.sender_role,
            'content': msg.message
            })
    response_text = response_chat(gpt_messages,prompt)

    gpt_chat = ChatMessage()
    gpt_chat.session = session
    gpt_chat.sender_role = 'assistant'
    gpt_chat.message = response_text
    gpt_chat.save()

    return Response({
        'session_id': session.pk,
        'bot_response': response_text,
    }, status=status.HTTP_200_OK)




