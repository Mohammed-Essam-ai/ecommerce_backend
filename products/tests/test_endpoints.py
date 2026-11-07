from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from products.models import (
    Product,
    Category,
    Brand,
    DressStyle,
    Review
)


class ProductEndpointsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user',password='123456')
        self.category = Category.objects.create(category_name='Casual')
        self.brand = Brand.objects.create(name='Nike')
        self.style = DressStyle.objects.create(name='Sport')
        self.product = Product.objects.create(product_name='T-Shirt',content='Cotton T-Shirt',price=250,category=self.category,brand=self.brand,style=self.style)
        self.review = Review.objects.create(user=self.user,product=self.product,comment='Very good product',rating=5)

    def test_get_products(self):
        url = reverse('products:product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_products_pagination(self):
        for i in range(12):
            Product.objects.create(product_name=f'Product {i}',content='Test product',price=100 + i,category=self.category,)
        url = reverse('products:product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']),10)

    def test_products_search(self):
        url = reverse('products:product-list')
        response = self.client.get(url,{'search': 'T-Shirt'})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['count'],1)

    def test_products_ordering(self):
        Product.objects.create(product_name='Expensive Product',price=1000,category=self.category)
        url = reverse('products:product-list')
        response = self.client.get(url,{'ordering': '-price'})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['price'],'1000.000')

    def test_get_product_details(self):
        url = reverse('products:product',kwargs={'product_id': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['product_name'],'T-Shirt')

    def test_get_categories(self):
        url = reverse('products:categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('categories', response.data)

    def test_get_product_reviews(self):

        url = reverse('products:reviews',kwargs={'product_id': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_create_review_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('products:reviews',kwargs={'product_id': self.product.id})
        data = {
            'product':self.product.id,
            'comment': 'Excellent product',
            'rating': 4
        }
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_create_review_unauthenticated_user(self):
        url = reverse('products:reviews',kwargs={'product_id': self.product.id})
        data = {
            'comment': 'Excellent product',
            'rating': 4
        }
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_create_review_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('products:reviews',kwargs={'product_id': self.product.id})
        data = {
            'comment': 'Bad rating',
            'rating': 10
        }
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_get_brands(self):
        url = reverse('products:brands')
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_styles(self):
        url = reverse('products:styles')
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_happy_reviews(self):
        url = reverse('products:happy-reviews')
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_happy_reviews_ordering(self):
        Review.objects.create(user=self.user,product=self.product,comment='Average product',rating=2)
        url = reverse('products:happy-reviews')
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual((response.data[0]['rating']),'5.0')

    def test_happy_reviews_maximum_10(self):
        for i in range(12):
            Review.objects.create(user=self.user,product=self.product,comment=f'Review {i}',rating=i % 6)
        url = reverse('products:happy-reviews')
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),10)
