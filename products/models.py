from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    category_name=models.CharField(max_length=50)
    photo=models.ImageField(upload_to='categories/',null=True)    
    def __str__(self):
        return self.category_name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)

    def __str__(self):
        return self.name


class DressStyle(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="dress_styles/", blank=True, null=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
        product_name=models.CharField(max_length=20)
        content=models.TextField(null=True,blank=True,verbose_name='Description') 
        price=models.DecimalField(max_digits=12,decimal_places=3) 
        image=models.ImageField(upload_to='products/')
        active=models.BooleanField(default=True)
        category=models.ForeignKey(Category,on_delete=models.CASCADE)
        brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True,blank=True,related_name="products")
        style = models.ForeignKey(DressStyle,on_delete=models.SET_NULL,null=True,blank=True,related_name="products")
        sizes = models.ManyToManyField(Size, blank=True, related_name="products")
        created_at = models.DateTimeField(auto_now_add=True)
        sold_count = models.PositiveIntegerField(default=0)

        def __str__(self): 
            return self.product_name 

        class Meta: 
            verbose_name='product'


class ProductColor(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="colors"
    )
    name = models.CharField(max_length=50)    

class ProductImage(models.Model):
    product_color = models.ForeignKey(
        ProductColor,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="products/")


class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviews')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    comment=models.TextField()
    rating = models.DecimalField(
    max_digits=2,
    decimal_places=1,
    validators=[
        MinValueValidator(0),
        MaxValueValidator(5),
    ],
    default=0
    )
    created_at=models.DateTimeField(auto_now_add=True)
