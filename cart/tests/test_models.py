from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from cart.models import Cart, CartItem
from products.models import Product, Category


class CartTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='Mohammed',email='test@gmail.com',password='123456')
        self.cart = Cart.objects.get(user=self.user)

    def test_create_cart(self):
        self.assertIsNotNone(self.cart)
        self.assertEqual(self.cart.user, self.user)

    def test_delete_user_cascade(self):
        cart_id = self.cart.id
        self.user.delete()
        self.assertFalse(Cart.objects.filter(id=cart_id).exists())


class CartItemTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='Mohammed',email='test@gmail.com',password='123456')

        self.cart = Cart.objects.get(user=self.user)

        self.category = Category.objects.create(category_name='casual')

        self.product = Product.objects.create(product_name='product_one',content='product content',price=100.0,category=self.category)

    def test_create_cart_item(self):
        item = CartItem.objects.create(product=self.product,cart=self.cart,quantity=2)
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.cart, self.cart)
        self.assertEqual(item.quantity, 2)

    def test_quantity_default(self):
        item = CartItem.objects.create(product=self.product,cart=self.cart)
        self.assertEqual(item.quantity, 1)

    def test_quantity_validation(self):
        item = CartItem(product=self.product,cart=self.cart,quantity=-1)

        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_delete_cart_cascade(self):
        item = CartItem.objects.create(product=self.product,cart=self.cart)
        cart_id = self.cart.id
        self.cart.delete()
        self.assertFalse(CartItem.objects.filter(cart_id=cart_id).exists())

    def test_delete_product_cascade(self):
        item = CartItem.objects.create(product=self.product,cart=self.cart)
        product_id = self.product.id
        self.product.delete()
        self.assertFalse(CartItem.objects.filter(product_id=product_id).exists())
