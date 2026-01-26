from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'        

class OrderItemSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source='product.product_name',read_only=True)
    class Meta:
        model=OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'created_at', 'items']
        read_only_fields = ['user', 'status', 'created_at']

class CreateOrderItemSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class CreateOrderSerializer(serializers.Serializer):
    items = CreateOrderItemSerializer(many=True)
    def create(self,validated_data):
        user=self.context['request'].user
        items=validated_data['items']
        order=Order.objects.create(user=user,total_price=0)
        total=0
        for item in items:
            product=Product.objects.get(id=item['product'])
            quantity=item['quantity']
            price=product.price*quantity
            orderitem=OrderItem.objects.create(order=order,product=product,quantity=quantity,price=price)
            total+=price            
        order.total_price=total
        order.save()
        return order    
