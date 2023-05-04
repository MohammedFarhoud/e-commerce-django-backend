from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from users.models import CustomUser

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wishlist',blank=True)
    product = models.ManyToManyField(Product, related_name='wishlists')
    
    def __str__(self):
        return self.user.username
    
    
    # def add_products(self, product_ids):
    #     products = [Product.objects.get(id=id) for id in product_ids]
    #     self.products.add(*products)