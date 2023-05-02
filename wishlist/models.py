from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from users.models import CustomUser

class Wishlist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ManyToManyField(Product, related_name='wishlists')
    
    def __str__(self):
        return self.user.username
