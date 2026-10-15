from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import  status
from .models import *
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.shortcuts import get_object_or_404


class CartItemView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        items = CartItem.objects.filter(cart=request.user.cart)
        serializer=CartItemSerializer(items,many=True)
        return Response(serializer.data)

    def post(self,request):
        print(request.data)
        serializer=CartItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(cart=request.user.cart)
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def IncreaseOne(request):
    cartitem_id = request.data.get("cartitem_id")
    cart=Cart.objects.get(user=request.user)
    cartitem=get_object_or_404(CartItem,id=cartitem_id,cart=cart)
    cartitem.quantity+=1
    cartitem.save()
    return Response(
        {
                'message': 'item icreased confirmed successfully',
                
            },
            status=status.HTTP_200_OK
    )   
 
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_item(request):
    cartitem_id = request.data.get("cartitem_id")
    item = get_object_or_404(
        CartItem,
        id=cartitem_id,
        cart=request.user.cart
    )

    item.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def DecreaseOne(request):
    cartitem_id = request.data.get("cartitem_id")
    cart=Cart.objects.get(user=request.user)
    cart_item=get_object_or_404(CartItem,id=cartitem_id,cart=cart)
    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:        
        cart_item.delete()
    return Response(
        {
                'message': 'item decreased confirmed successfully',
                
            },
            status=status.HTTP_200_OK
    )   

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart_item_quantity(request):
    print(request.data)
    cartitem_id=request.GET.get("cartitem_id")
    item = get_object_or_404(
        CartItem,
        id=cartitem_id,
        cart=request.user.cart
    )
    return Response({"quantity":item.quantity})