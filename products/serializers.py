from rest_framework import serializers
from .models import Category,Product, Image

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Image
        fields= ['image']
        
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = ImageSerializer(many=True)
    is_in_cart = serializers.SerializerMethodField()
    is_in_wishlist = serializers.SerializerMethodField()
    
    class Meta:
        model=Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'category', 'images', 'is_in_cart', 'is_in_wishlist']
        
    def get_is_in_cart(self, obj):
        user = self.context['request'].user
        return user.cart.products.filter(id=obj.id).exists()

    def get_is_in_wishlist(self, obj):
        user = self.context['request'].user
        return user.wishlist.product.filter(id=obj.id).exists()