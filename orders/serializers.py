from rest_framework import serializers
from orders.models import Order
from products.serializers import ProductSerializer

class PostOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = '__all__'
        
class GetOrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id','status', 'payment_method', 'products']