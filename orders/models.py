from django.db import models
from products.models import Product

from users.models import CustomUser
from django.core.validators import MinValueValidator


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='order')
    product = models.ManyToManyField(Product, related_name='orders',through='OrderProduct')
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
    )
    status = models.CharField(max_length=9, choices=STATUS_CHOICES)
    
    def __str__(self):
        return f"{self.user.username} - #{self.pk}"
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])


    def __str__(self):
        return self.product.name
    
