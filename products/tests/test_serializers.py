from django.test import TestCase
from django.contrib.auth.models import User
from products.models import (
    Category, Brand, DressStyle, Size,
    Product, ProductColor, ProductImage, Review
)
from products.serializers import (
    CategorySerializer,
    SizeImageSerializer,
    ProductColorSerializer,
    ProductImageSerializer,
    BrandSerializer,
    DressStyleSerializer,
    SizeSerializer,
    ProductSerializer,
    ReviewSerializer
)


class TestSerializer(TestCase):

    def setUp(self):
        self.category = Category.objects.create(category_name="Men")
        self.brand = Brand.objects.create(name="Nike")
        self.style = DressStyle.objects.create(name="Casual")
        self.size = Size.objects.create(name="XL")
        self.product = Product.objects.create(product_name="T-Shirt",price=250,category=self.category,brand=self.brand,style=self.style)
        self.product.sizes.add(self.size)
        self.color = ProductColor.objects.create(product=self.product,name="Black")
        self.image = ProductImage.objects.create(product_color=self.color,image="test.jpg")
        self.user = User.objects.create_user(username="testuser",password="test12345")
        self.review = Review.objects.create(user=self.user,product=self.product,comment="Very good",rating=4.5)
    
    def test_category_serializer(self):
        serializer=CategorySerializer(self.category)
        self.assertEqual(serializer.data['category_name'],'Men')

    def test_brand_serializer(self):
        serializer = BrandSerializer(self.brand)
        self.assertEqual(serializer.data["name"], "Nike")

    def test_style_serializer(self):
        serializer = DressStyleSerializer(self.style)
        self.assertEqual(serializer.data["name"], "Casual")

    def test_size_serializer(self):
        serializer = SizeSerializer(self.size)
        self.assertEqual(serializer.data["name"], "XL")

    def test_product_image_serializer(self):
        serializer = ProductImageSerializer(self.image)
        self.assertEqual(serializer.data["product_color"],self.color.id)

    def test_product_color_serializer(self):
        serializer = ProductColorSerializer(self.color)
        self.assertEqual(serializer.data["name"], "Black")
        self.assertEqual(len(serializer.data["images"]), 1)

    def test_product_serializer(self):
        serializer = ProductSerializer(self.product)
        data = serializer.data
        self.assertEqual(data["product_name"], "T-Shirt")
        self.assertEqual(data["category"]["category_name"],"Men")
        self.assertEqual(data["brand"]["name"],"Nike")
        self.assertEqual(data["style"]["name"],"Casual")
        self.assertEqual(data["sizes"][0]["name"],"XL")
        self.assertEqual(data["colors"][0]["name"],"Black")

    def test_review_serializer(self):
        serializer = ReviewSerializer(self.review)
        self.assertEqual(serializer.data["user_name"],"testuser")
        self.assertEqual(serializer.data["comment"],"Very good")
        self.assertEqual(float(serializer.data["rating"]),4.5)

    def test_review_invalid_rating(self):
        data = {
            "product": self.product.id,
            "comment": "Bad review",
            "rating": 6
        }
        serializer = ReviewSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("rating", serializer.errors)

    def test_review_valid_data(self):
        data = {
            "product": self.product.id,
            "comment": "Excellent",
            "rating": 4.5
        }
        serializer = ReviewSerializer(data=data)
        self.assertTrue(serializer.is_valid(),serializer.errors)