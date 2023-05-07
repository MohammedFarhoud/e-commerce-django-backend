from django.db import models
from products.models import Product
from users.models import CustomUser
from django.core.validators import MinValueValidator

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')
    products = models.ManyToManyField(Product, related_name='carts', through='CartProduct')
    
    def __str__(self):
        return f"{self.user.username} - #{self.pk}"
    
    def calculate_total_price(self):
        total_price = 0
        cart_products = self.cartproduct_set.all()
        for cart_product in cart_products:
            total_price += cart_product.product.price * cart_product.quantity
        return total_price

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)], default=1)