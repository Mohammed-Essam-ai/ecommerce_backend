from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    category_name=models.CharField(max_length=50)
    photo=models.ImageField(upload_to='photos/%y/%m/%d',null=True)    
    def __str__(self):
        return self.category_name

class Product(models.Model):
        product_name=models.CharField(max_length=20)
        content=models.TextField(null=True,blank=True,verbose_name='Description') 
        price=models.DecimalField(max_digits=12,decimal_places=3) 
        image=models.ImageField(upload_to='photos/%y/%m/%d')
        active=models.BooleanField(default=True)
        category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
        url=models.TextField(null=True)
        def __str__(self): 
            return self.product_name        
        class Meta: 
            verbose_name='product'
            ordering=['price']

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Order #{self.id} - {self.status}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

