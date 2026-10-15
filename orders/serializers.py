from rest_framework import serializers
from .models import *
from cart.models import Cart,CartItem
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']
        read_only_fields = ['price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'total_price',
            'status',
            'created_at',
            'items'
        ]
        read_only_fields = [
            'user',
            'total_price',
            'status',
            'created_at'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        order = Order.objects.create(
            user=user,
            total_price=0
        )

        total = 0

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            price = product.price * quantity

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )

            total += price

        order.total_price = total
        order.save()

        return order