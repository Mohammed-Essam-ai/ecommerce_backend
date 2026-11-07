from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from orders.models import Order, OrderItem
from products.models import Product, Category, Brand, DressStyle
from cart.models import Cart, CartItem


class OrderEndpointsTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user',password='123456')
        self.other_user = User.objects.create_user(username='other_user',password='123456')
        self.category = Category.objects.create(category_name='Clothes')
        self.brand = Brand.objects.create(name='Nike')
        self.style = DressStyle.objects.create(name='Casual')
        self.product = Product.objects.create(product_name='T-Shirt',price=250,category=self.category,brand=self.brand,style=self.style)
        self.cart = Cart.objects.get(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart,product=self.product,quantity=2)
        self.client.force_authenticate(user=self.user)
        self.order = Order.objects.create(user=self.user,total_price=500,status='pending')
        self.order_item = OrderItem.objects.create(order=self.order,product=self.product,quantity=2,price=250)

    def test_get_orders(self):
        url = reverse('orders:orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'],self.order.id)

    def test_get_orders_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse('orders:orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_checkout(self):
        url = reverse('orders:checkout')
        response = self.client.post(
            url,
            {},
            format='json'
        )
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'],'Order created successfully')
        self.assertEqual(response.data['total_price'],500)
        self.assertEqual(response.data['status'],'pending')


    def test_checkout_empty_cart(self):
        self.cart.cartitems.all().delete()
        url = reverse('orders:checkout')
        response = self.client.post(
            url,
            {},
            format='json'
        )
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'],'Cart is empty')

    def test_confirm_order(self):
        url = reverse(
            'orders:confirm-order',
            kwargs={'order_id': self.order.id}
        )
        response = self.client.post(
            url,
            {},
            format='json'
        )
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['message'],'Order confirmed successfully')
        self.order.refresh_from_db()
        self.assertEqual(self.order.status,'paid')
        self.product.refresh_from_db()

        self.assertEqual(self.product.sold_count,2)
        self.assertEqual(self.cart.cartitems.count(),0)

    def test_confirm_order_not_found(self):
        url = reverse(
            'orders:confirm-order',
            kwargs={'order_id': 99999}
        )
        response = self.client.post(
            url,
            {},
            format='json'
        )
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_confirm_other_user_order(self):
        other_order = Order.objects.create(user=self.other_user,total_price=100,status='pending')
        url = reverse(
            'orders:confirm-order',
            kwargs={'order_id': other_order.id}
        )
        response = self.client.post(
            url,
            {},
            format='json'
        )
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_cancel_order(self):
        url = reverse(
            'orders:cancel-order',
            kwargs={'order_id': self.order.id}
        )
        response = self.client.post(
            url,
            {},
            format='json'
        )
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['message'],'Order cancelled successfully')
        self.order.refresh_from_db()
        self.assertEqual(self.order.status,'failed')

    def test_cancel_order_not_found(self):
        url = reverse(
            'orders:cancel-order',
            kwargs={'order_id': 99999}
        )
        response = self.client.post(
            url,
            {},
            format='json'
        )
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_cancel_other_user_order(self):
        other_order = Order.objects.create(user=self.other_user,total_price=100,status='pending')
        url = reverse(
            'orders:cancel-order',
            kwargs={'order_id': other_order.id}
        )
        response = self.client.post(
            url,
            {},
            format='json'
        )
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)