from django.shortcuts import render
from .models import Product,Category
from django.http import HttpResponse ,JsonResponse
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import  status
from .serializers import *
from django.views.generic import View


class ProductView(APIView):
      permission_classes = []        
      def get(self,request,product_id):
        product=Product.objects.get(id=product_id)
        product_info=ProductSerializer(product).data
        return Response(product_info)
      
class ProductListView(APIView):
    permission_classes = []
    def get(self,request,category_id):
        products=Product.objects.filter(category_id=category_id)
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class CategoryListView(APIView):
    permission_classes = []
    def get(self,request):
        categories=Category.objects.all()
        serializer=CategorySerializer(categories,many=True)
        return Response({'categories':serializer.data})

class CreateOrderView(APIView):
    def post(self,request):
        serializer=CreateOrderSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"seccessful action."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderListView(APIView):    
    def get(self,request):
        serializer=OrderSerializer
        orders=Order.objects.filter(user=self.request.user)
        serializer=OrderSerializer(orders,many=True)
        return Response(serializer.data) 

