from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import  status
from .serializers import *
from django.views.generic import View
from rest_framework.permissions import AllowAny,IsAuthenticated
from cart.models import Cart ,CartItem
from django.contrib.auth.models import User


class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)



class CheckoutView(APIView):
    def post(self, request):

        cart = get_object_or_404(
            Cart,
            user=request.user
        )

        cart_items = cart.cartitems.select_related('product')

        if not cart_items.exists():
            return Response(
                {'detail': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        
        order = Order.objects.create(
            user=request.user,
            total_price=0,
            status='pending'
        )

        total_price = 0

       
        for cart_item in cart_items:

            price = cart_item.product.price
            quantity = cart_item.quantity

            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=quantity,
                price=price
            )

            total_price += price * quantity

        
        order.total_price = total_price
        order.save()

        return Response(
            {
                'message': 'Order created successfully',
                'order_id': order.id,
                'total_price': total_price,
                'status': order.status
            },
            status=status.HTTP_201_CREATED
        )


class ConfirmOrderView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, order_id):

        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user
        )

        order.status = 'paid'
        order.save()

        cart = get_object_or_404(
            Cart,
            user=request.user
        )

        items=cart.items.all()
        
        for item in items:
            product=item.product
            product.sold_count+=item.quantity
            product.save(update_fields=["sold_count"])

        cart.cartitems.all().delete()

        return Response(
            {
                'message': 'Order confirmed successfully',
                'order_id': order.id,
                'total_price': order.total_price,
                'status': order.status
            },
            status=status.HTTP_200_OK
        )


class CancelOrderView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, order_id):

        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user
        )

        order.status = 'failed'
        order.save()

        return Response(
            {
                'message': 'Order cancelled successfully'
            },
            status=status.HTTP_200_OK
        )
        