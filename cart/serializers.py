from rest_framework import serializers
from cart.models import Cart, CartProduct
from products.models import Product
from django.shortcuts import get_object_or_404
from users.models import CustomUser


class CartSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Cart
        fields = '__all__'
        
    def create(self, validated_data):
        product = validated_data['products'][0]
        existing_product = get_object_or_404(Product, id=product.id)
        user = self.context.get('user')
        cart, created = Cart.objects.get_or_create(user=user)
        cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=existing_product)
        if not created:
            cart_product.quantity += 1
            cart_product.save()
        else:
            cart.products.add(existing_product)
        return cart
    
    # def update(self, instance, validated_data):
    #     product = validated_data['products'][0]
    #     product = get_object_or_404(Product, id=product.id)
    #     existing_product = instance.products.filter(id=product.id).first()
    #     if existing_product:
    #         quantity += 1
    #         existing_product.save()
    #     else:
    #         instance.products.add(product)
    #     return
        