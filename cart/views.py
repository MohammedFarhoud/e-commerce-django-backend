from cart.serializers import CartSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from cart.models import Cart, CartProduct
from django.shortcuts import get_object_or_404
from rest_framework import status, serializers

class CartView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        
        serializer = CartSerializer(data=request.data, context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product added successfully', 'cart': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, *args, **kwargs):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        serializer = CartSerializer(cart)
        return Response({'message': 'Cart found', 'cart': serializer.data}, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        user = request.user
        action = request.data.get('action')
        product = request.data.get('product')
        
        cart, created = Cart.objects.get_or_create(user=user)
        
        try:
            cart_product = CartProduct.objects.get(cart=cart, product=product)
        except CartProduct.DoesNotExist:
            raise serializers.ValidationError({'message': 'Product not found'}, code=status.HTTP_404_NOT_FOUND)
        
        serializer = CartSerializer(cart_product, data=request.data, context={'action': action})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product Updated successfully', 'cart': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        product_id = kwargs['product']
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        product = get_object_or_404(Product, id=product_id)
        cart_product = get_object_or_404(CartProduct, cart=cart, product=product)
        cart_product.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)