from django.db import models
from products.models import Product
from users.models import CustomUser

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')
    product = models.ManyToManyField(Product, related_name='carts')
    
    def __str__(self):
        return f"{self.user.username} - #{self.pk}"
    