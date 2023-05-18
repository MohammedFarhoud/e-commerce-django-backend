from rest_framework import serializers

from users.models import CustomUser
from django.contrib.auth.models import AnonymousUser


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
        if isinstance(user, AnonymousUser):
            return False
        try:
            return user.cart.products.filter(id=obj.id).exists()
        except CustomUser.cart.RelatedObjectDoesNotExist:
            return False


    def get_is_in_wishlist(self, obj):
        user = self.context['request'].user
        if isinstance(user, AnonymousUser):
            return False
        try:
            return user.wishlist.product.filter(id=obj.id).exists()
        except CustomUser.cart.RelatedObjectDoesNotExist:
            return False