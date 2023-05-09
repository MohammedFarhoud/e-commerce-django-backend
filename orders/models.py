from django.db import models
from products.models import Product
from users.models import CustomUser
from django.core.validators import MinValueValidator
from users.models import CustomUser


class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )
    PAYMENT_METHOD_CHOICES = (
        ('cod', 'Cash on Delivery'),
        ('visa', 'Pay by Visa'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='order')
    products = models.ManyToManyField(Product, related_name='orders',through='OrderProduct')
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=16, choices=PAYMENT_METHOD_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - #{self.pk}"
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])

class PaymentHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments',blank=True)
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    date=models.DateTimeField(auto_now_add=True)
    payment_status=models.BooleanField()


    def __str__(self):
        return self.product.name
    
