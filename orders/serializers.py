from rest_framework import serializers
import orders
from orders.models import Order
from products.serializers import ProductSerializer
from rest_framework.request import Request

class PostOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = '__all__'
        
# class GetOrderSerializer(serializers.ModelSerializer):
#     products = ProductSerializer(many=True)

    # class Meta:
    #     model = Order
    #     fields = ['id','status', 'payment_method', 'products']
        

class GetOrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, context={'request': None})

    class Meta:
        model = Order
        fields = ['id', 'status', 'payment_method', 'products']

# serializer = GetOrderSerializer(orders, many=True, context={'request': request})
serializer = GetOrderSerializer(orders, many=True, context={'request': Request})
