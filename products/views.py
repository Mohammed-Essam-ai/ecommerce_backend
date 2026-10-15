from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import  status
from .serializers import *
from django.views.generic import View
from rest_framework.permissions import AllowAny,IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view , permission_classes
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class ProductListView(ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = ProductFilter

    search_fields = ['name', 'description']

    ordering_fields = ['price', 'created_at', 'rating']

    pagination_class = ProductPagination


class ProductView(APIView):
      permission_classes = [AllowAny]        
      def get(self,request,product_id):
        product=Product.objects.get(id=product_id)
        product_info=ProductSerializer(product).data
        return Response(product_info)


class CategoryListView(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        categories=Category.objects.all()
        serializer=CategorySerializer(categories,many=True)
        return Response({'categories':serializer.data})


class ReviewView(APIView):
    def get_permissions(self):
        if self.request.method=='POST':
            return [IsAuthenticated()]
        else:
            return [AllowAny()]    
    def get(self,request,product_id):
        product = get_object_or_404(Product, id=product_id)
        reviews = product.reviews.all()
        serializer =ReviewSerializer(reviews,many=True)
        return Response(serializer.data)
    def post(self,request,product_id):
        product = get_object_or_404(Product, id=product_id)    
        serializer=ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user,product=product)
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)   


@api_view(["GET"])
def get_happy_reviews(request):
    reviews=Review.objects.order_by("-rating")[:10]
    serializer=ReviewSerializer(reviews,many=True)
    return Response(serializer.data) 


@api_view(["GET"])
def get_brands(request):
    brands = Brand.objects.all()
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_styles(request):
    styles = DressStyle.objects.all()
    serializer = DressStyleSerializer(styles, many=True)
    return Response(serializer.data)
