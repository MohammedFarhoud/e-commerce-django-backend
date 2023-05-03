from rest_framework import serializers
from .models import Wishlist
from products.serializers import ProductSerializer
class WishlistSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', many=True, read_only=True)


    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'product_details']
