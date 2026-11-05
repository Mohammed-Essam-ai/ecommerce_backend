from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from products.models import Product, Category
from orders.models import Order, OrderItem
from orders.serializers import OrderItemSerializer, OrderSerializer


class OrderItemSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user',password='123456')
        self.category = Category.objects.create(category_name='test_category')
        self.product = Product.objects.create(product_name='test_product',content='test_content',price=100,category=self.category)
        self.order = Order.objects.create(user=self.user,total_price=100)
        self.order_item = OrderItem.objects.create(order=self.order,product=self.product,quantity=1,price=100)

    def test_serialize_order_item(self):
        serializer = OrderItemSerializer(self.order_item)
        self.assertEqual(serializer.data['product'], self.product.id)
        self.assertEqual(serializer.data['quantity'], 1)
        self.assertEqual(float(serializer.data['price']), 100.0)



class OrderSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user',password='123456')
        self.factory = APIRequestFactory()
        self.request = self.factory.post('/orders/')
        self.request.user = self.user
        self.category = Category.objects.create(category_name='test_category')
        self.product1 = Product.objects.create(product_name='product_one',content='content_one',price=100,category=self.category)
        self.product2 = Product.objects.create(product_name='product_two',content='content_two',price=200,category=self.category)

    def test_create_order(self):
        data = {
            'items': [
                {
                    'product': self.product1.id,
                    'quantity': 2
                },
                {
                    'product': self.product2.id,
                    'quantity': 3
                }
            ]
        }
        serializer = OrderSerializer(data=data,context={'request': self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total_price, 800)
        self.assertEqual(order.items.count(), 2)

    def test_order_items_prices(self):
        data = {
            'items': [
                {
                    'product': self.product1.id,
                    'quantity': 2
                },
                {
                    'product': self.product2.id,
                    'quantity': 3
                }
            ]
        }
        serializer = OrderSerializer(data=data,context={'request': self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()
        item1 = order.items.get(product=self.product1)
        item2 = order.items.get(product=self.product2)
        self.assertEqual(item1.price, 200)
        self.assertEqual(item2.price, 600)

    def test_read_only_fields(self):
        data = {
                'user': self.user.id,
                'total_price': 9999,
                'status': 'completed',
                'items': [
                    {
                        'product': self.product1.id,
                        'quantity': 1
                    }
                ]
                }
        serializer = OrderSerializer(data=data,context={'request': self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn('user', serializer.validated_data)
        self.assertNotIn('total_price', serializer.validated_data)
        self.assertNotIn('status', serializer.validated_data)

    def test_serialize_order(self):
        order = Order.objects.create(user=self.user,total_price=200)
        OrderItem.objects.create(order=order,product=self.product1,quantity=2,price=200)
        serializer = OrderSerializer(order)
        self.assertEqual(serializer.data['user'], self.user.id)
        self.assertEqual(float(serializer.data['total_price']), 200.0)
        self.assertEqual(len(serializer.data['items']), 1)
