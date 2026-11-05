from django.contrib.auth.models import User
from orders.models import Order , OrderItem
from django.test import TestCase
from products.models import Product,Category


class TestOrder(TestCase):

    def setUp(self):
        self.username='Mohammed_Essam'
        self.email='mohammed13@gmail.com'
        self.password=123#mo.@!123
        self.user=User.objects.create(username=self.username,email=self.email,password=self.password)

    def test_create_order(self):
        self.order=Order.objects.create(user=self.user,total_price=0)
        self.assertEqual(self.user,self.order.user)

    def test_order_default_status(self):
        self.order=Order.objects.create(user=self.user,total_price=0)
        self.assertEqual(self.order.status,'pending')    

class testOrderItem(TestCase):

    def setUp(self):
        self.username='Mohammed_Essam'
        self.email='mohammed13@gmail.com'
        self.password=123#mo.@!123
        self.user=User.objects.create(username=self.username,email=self.email,password=self.password)
        self.order=Order.objects.create(user=self.user,total_price=0)

    def test_create_order_item(self):
        category=Category.objects.create(category_name='casual')
        product=Product.objects.create(product_name='',price=100.0,category=category,image='test.png')
        order_item=OrderItem.objects.create(order=self.order,product=product,price=100.0,quantity=2)
        self.assertEqual(order_item.quantity,2)
        self.assertEqual(order_item.price,100.0)
        self.assertEqual(order_item.product,product)