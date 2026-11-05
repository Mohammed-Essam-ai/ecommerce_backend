from django.test import TestCase
from products.models import Category,DressStyle, Brand, Product, ProductColor, ProductImage , Size, Review
from django.db import IntegrityError
from django.contrib.auth.models import User



class CategoryTest(TestCase):

    def test_create_category(self):
        self.category=Category.objects.create(category_name='test_photo')
        self.assertEqual(self.category.category_name,'test_photo')



class BrandTest(TestCase):

    def test_create_brand(self):
        brand = Brand.objects.create(name="Nike")
        self.assertEqual(str(brand), "Nike")
    def test_product_image_constrains(self):
        brand = Brand.objects.create(name="Nike")
        with self.assertRaises(IntegrityError):
            new_brand=Brand.objects.create(name="Nike")


class DressStyleTest(TestCase):

    def test_create_dressstyle(self):
        self.style=DressStyle.objects.create(name='casual')
        self.assertEqual(self.style.name,'casual')



class SizeTest(TestCase):

    def test_create_size(self):
        size = Size.objects.create(name="XL")
        self.assertEqual(str(size), "XL")



class ProductTest(TestCase):
    
    def setUp(self):
        self.category=Category.objects.create(category_name='casual')
        self.product=Product.objects.create(product_name='product_one',content='content_one',price=100.0,category=self.category)
    
    def test_create_product(self):
        self.assertEqual(self.product.product_name,'product_one')
        self.assertEqual(self.product.price,100.0)
        self.assertEqual(self.product.category,self.category)

    def test_product_default_values(self):    
        self.assertTrue(self.product.active)
        self.assertEqual(self.product.sold_count,0)

    def test_product_sizes(self):
        size=Size.objects.create(name='XL')
        self.product.sizes.add(size)
        self.assertIn(size,self.product.sizes.all())    



class ProductColorTest(TestCase):

    def test_product_color(self):
        category = Category.objects.create(category_name="Men")
        product = Product.objects.create(product_name="Shirt",price=200,category=category)
        color = ProductColor.objects.create(product=product,name="Black")
        self.assertEqual(color.product, product)
        self.assertIn(color, product.colors.all())   
        


class ProductImageTest(TestCase):

    def test_product_image_relationship(self):
        category = Category.objects.create(category_name="Men")
        product = Product.objects.create(product_name="Shirt",price=200,category=category)
        color = ProductColor.objects.create(product=product,name="Black")
        image = ProductImage.objects.create(product_color=color,image="products/test.jpg")
        self.assertEqual(image.product_color, color)
        self.assertIn(image, color.images.all())
    
        


class ReviewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser",password="test12345")
        self.category = Category.objects.create(category_name="Men")
        self.product = Product.objects.create(            product_name="Shirt",price=200,category=self.category)

    def test_create_review(self):
        review = Review.objects.create(user=self.user,product=self.product,comment="Good product",rating=4.5)
        self.assertEqual(review.rating, 4.5)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.product, self.product)

