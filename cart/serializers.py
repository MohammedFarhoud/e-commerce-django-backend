from rest_framework import serializers
from cart.models import Cart, CartProduct, Product
from cart.pagination import CartProductPagination
from products.serializers import ProductSerializer
from django.core.validators import MinValueValidator
from django.shortcuts import get_object_or_404

class AddToCartSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(validators=[MinValueValidator(1)], default=1)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartProduct
        fields = ['product', 'quantity', 'total_price']
        
    def get_total_price(self, instance):
        user = self.context.get('user')
        cart = user.cart
        return cart.calculate_total_price()
        
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
        if (cart_product.quantity <= product.quantity):
            cart_product.save()
        else:
            raise serializers.ValidationError({'error': "You exceeded product quantity in our store."})

        return cart_product
    
class UpdateCartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartProduct
        fields = ['product', 'quantity', 'total_price']
        
    def get_total_price(self, instance):
        cart = instance.cart
        return cart.calculate_total_price()
        
    def update(self, instance ,validated_data):
        action = self.context.get('action')
        product_id = self.context.get('product')
        prodcut = get_object_or_404(Product, id=product_id)
        if action not in ('INCREASE', 'DECREASE'):
            raise serializers.ValidationError({'error': "Action can only be 'INCREASE' or 'DECREASE'"})
        
        if action == 'INCREASE':
            instance.quantity += 1
        elif action == 'DECREASE' and instance.quantity > 0:
            instance.quantity -= 1
        
        if (instance.quantity <= prodcut.quantity):
            instance.save()
        else:
            raise serializers.ValidationError({'error': "You exceeded product quantity in our store."})
        instance.save()
        
        if instance.quantity == 0:
            instance.delete()
            
        return instance

class CartSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, instance):
            return instance.calculate_total_price()
        
    def get_products(self, instance):
        cart_products = instance.cartproduct_set.all()
        request = self.context.get('request')
        paginator = CartProductPagination()
        paginated_products = paginator.paginate_queryset(cart_products, request)

        products = []
        for cart_product in paginated_products:
            images = [image.image.url for image in cart_product.product.images.all()]
            products.append({
                'id': cart_product.product.id,
                'name': cart_product.product.name,
                'description': cart_product.product.description,
                'images': images,
                'price': cart_product.product.price,
                'category': cart_product.product.category.name,
                'total_quantity': cart_product.product.quantity,
                'quantity': cart_product.quantity,
            })
        return paginator.get_paginated_response(products).data
    
    class Meta:
        model = Cart
        fields = ['id', 'products', 'total_price']
