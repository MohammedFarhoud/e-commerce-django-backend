from rest_framework import serializers
from cart.models import Cart, CartProduct
from django.shortcuts import get_object_or_404

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartProduct
        fields = ['product', 'quantity']
        
    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']
        user = self.context.get('user')
        
        cart, created = Cart.objects.get_or_create(user=user)
        cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_product.quantity += quantity
        else:
            cart_product.quantity = quantity

        cart_product.save()
            
        return cart_product
    
    def update(self, instance ,validated_data):
        action = self.context.get('action')
        if action not in ('INCREASE', 'DECREASE'):
            raise serializers.ValidationError({'error': "Action can only be 'INCREASE' or 'DECREASE'"})
        
        if action == 'INCREASE':
            instance.quantity += 1
        elif action == 'DECREASE' and instance.quantity > 0:
            instance.quantity -= 1
        instance.save()
        
        if instance.quantity == 0:
            instance.delete()
            
        return instance
