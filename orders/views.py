from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from cart.models import Cart
from orders.models import Order, OrderProduct
from orders.serializers import GetOrderSerializer, PostOrderSerializer
from rest_framework import status
from rest_framework.response import Response


class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        payment_method = request.data.get('payment_method')
        total_price = cart.calculate_total_price()
        cart_products = cart.cartproduct_set.all()
        order_data = {
            'user': request.user.id,
            'payment_method': payment_method,
        }
        serializer = PostOrderSerializer(data=order_data)
        if serializer.is_valid():
            order = serializer.save()
            for cart_product in cart_products:
                OrderProduct.objects.create(order=order, product=cart_product.product, quantity=cart_product.quantity)
            cart.delete()
            return Response({'message': 'Order added successfully', 'order': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
    def put(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        if order.status == 'PENDING':
            order.status = 'CANCELLED'
            order.save()
            return Response({'message': 'Order cancelled successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Order status should be pending to cancel'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        if not orders:
            return Response({'error': 'No orders found for the user'}, status=status.HTTP_404_NOT_FOUND)
        serializer = GetOrderSerializer(orders, many=True)
        return Response({'message': 'Orders found', 'orders': serializer.data}, status=status.HTTP_200_OK)
