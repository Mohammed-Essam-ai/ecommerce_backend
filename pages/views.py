from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['GET'])
def home(request):
      HttpResponse('hello')
      return Response({'message':'home'})
      return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def about(request):
      return Response(status=status.HTTP_200_OK)
