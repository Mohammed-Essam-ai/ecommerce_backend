from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class SizeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields="__all__"

class ProductColorSerializer(serializers.ModelSerializer):
    images = SizeImageSerializer(many=True, read_only=True)
    class Meta:
        model=ProductColor
        fields='__all__' 


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields='__all__' 


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields='__all__'    


class DressStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model=DressStyle
        fields='__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Size
        fields='__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()
    style = DressStyleSerializer()
    sizes = SizeSerializer(many=True)
    colors=ProductColorSerializer(many=True)
    class Meta:
        model=Product
        fields='__all__' 

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)
    class Meta:
        model=Review
        fields='__all__'
        read_only_fields=['user','created_at',"user_name"]

 