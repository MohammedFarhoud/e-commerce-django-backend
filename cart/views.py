from django.shortcuts import render
from cart.serializers import CartSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from cart.models import Cart, CartProduct
from django.shortcuts import get_object_or_404
from rest_framework import status

class CartView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = CartSerializer(data={'products': [request.data.get('product')]}, context={'user': user})
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
        
    def delete(self, request, *args, **kwargs):
        product_id = kwargs['product']
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        product = get_object_or_404(Product, id=product_id)
        cart_product = get_object_or_404(CartProduct, cart=cart, product=product)
        if cart_product.quantity > 1:
            cart_product.quantity -= 1
            cart_product.save()
        else:
            cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)