from django.shortcuts import render
from rest_framework.decorators import api_view
from .utils import prompt

# Create your views here.
@api_view(['GET'])
def test(request):
    pass
