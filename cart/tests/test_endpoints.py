from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from cart.models import Cart, CartItem
from products.models import Product, Category


class CartEndpointsTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user',password='123456')
        self.cart, _ = Cart.objects.get_or_create(user=self.user)
        self.category = Category.objects.create(category_name='Clothes')
        self.product = Product.objects.create(product_name='T-Shirt',content='Cotton T-Shirt',price=250,category=self.category)
        self.cart_item = CartItem.objects.create(cart=self.cart,product=self.product,quantity=2)
        self.client.force_authenticate(user=self.user)

    def test_get_cart_items(self):
        url = reverse('cart:cart-items')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['quantity'],2)

    def test_add_cart_item(self):
        url = reverse('cart:cart-items')
        data = {
            'product_id': self.product.id,
            'quantity': 3
        }
        response = self.client.post(
            url,
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.filter(cart=self.cart).count(),2)

    def test_add_cart_item_invalid_data(self):
        url = reverse('cart:cart-items')

        data = {
            'product_id': 99999,
            'quantity': 2
        }

        response = self.client.post(
            url,
            data,
            format='json'
        )

        self.assertEqual(response.status_code, 400)

    def test_increase_quantity(self):
        url = reverse('cart:increase-one')

        data = {
            'cartitem_id': self.cart_item.id
        }
        response = self.client.patch(url,data,format='json')
        self.cart_item.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.cart_item.quantity, 3)

    def test_increase_item_not_found(self):
        url = reverse('cart:increase-one')
        response = self.client.patch(
            url,
            {'cartitem_id': 99999},
            format='json'
        )
        self.assertEqual(response.status_code, 404)

    def test_decrease_quantity(self):
        url = reverse('cart:decrease-one')
        response = self.client.patch(
            url,
            {'cartitem_id': self.cart_item.id},
            format='json'
        )
        self.cart_item.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.cart_item.quantity, 1)

    def test_decrease_quantity_to_zero_deletes_item(self):
        self.cart_item.quantity = 1
        self.cart_item.save()
        url = reverse('cart:decrease-one')
        response = self.client.patch(
            url,
            {'cartitem_id': self.cart_item.id},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CartItem.objects.filter(id=self.cart_item.id).exists())

    def test_delete_cart_item(self):
        url = reverse('cart:delete-item')
        response = self.client.delete(
            url,
            {'cartitem_id': self.cart_item.id},
            format='json'
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(CartItem.objects.filter(id=self.cart_item.id).exists())

    def test_delete_item_not_found(self):
        url = reverse('cart:delete-item')

        response = self.client.delete(
            url,
            {'cartitem_id': 99999},
            format='json'
        )
        self.assertEqual(response.status_code, 404)


    def test_get_cart_item_quantity(self):
        url = reverse('cart:cart-item-quantity')
        response = self.client.get(
            url,
            {'cartitem_id': self.cart_item.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['quantity'], 2)

    def test_get_quantity_item_not_found(self):
        url = reverse('cart:cart-item-quantity')
        response = self.client.get(
            url,
            {'cartitem_id': 99999}
        )
        self.assertEqual(response.status_code, 404)

    def test_unauthenticated_user_cannot_access_cart(self):
        self.client.force_authenticate(user=None)
        urls = [
            reverse('cart:cart-items'),
            reverse('cart:increase-one'),
            reverse('cart:decrease-one'),
            reverse('cart:delete-item'),
            reverse('cart:cart-item-quantity'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 401)

    