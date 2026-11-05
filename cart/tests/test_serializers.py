from django.test import TestCase
from django.contrib.auth.models import User
from cart.models import Cart, CartItem
from products.models import Product, Category
from cart.serializers import CartItemSerializer, CartSerializer


class CartItemSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user',password='123456')
        self.category = Category.objects.create(category_name='test_category')
        self.product = Product.objects.create(product_name='test_product',content='test_content',price=100,category=self.category)
        self.cart = Cart.objects.get(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart,product=self.product,quantity=2)

    def test_serialize_cart_item(self):
        serializer = CartItemSerializer(self.cart_item)
        self.assertEqual(serializer.data['product']['id'], self.product.id)
        self.assertEqual(serializer.data['quantity'], 2)

    def test_product_id_is_write_only(self):
        serializer = CartItemSerializer(self.cart_item)
        self.assertNotIn('product_id', serializer.data)

    def test_create_cart_item_using_product_id(self):
        data = {
            'product_id': self.product.id,
            'quantity': 3
        }
        serializer = CartItemSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data['product'], self.product)
        self.assertEqual(serializer.validated_data['quantity'], 3)


class CartSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user',password='123456')
        self.category = Category.objects.create(category_name='test_category')
        self.product = Product.objects.create(product_name='test_product',content='test_content',price=100,category=self.category)
        self.cart = Cart.objects.get(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart,product=self.product,quantity=2)

    def test_serialize_cart(self):
        serializer = CartSerializer(self.cart)
        self.assertEqual(serializer.data['id'], self.cart.id)

