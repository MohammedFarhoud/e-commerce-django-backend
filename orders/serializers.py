from rest_framework import serializers
import orders
from orders.models import Order, OrderProduct
from products.serializers import ProductSerializer
from rest_framework.request import Request
from django.db import models

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
    # products = ProductSerializer(many=True, context={'request': None})
    total_quantity = serializers.SerializerMethodField()
    order_price = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    

    class Meta:
        model = Order
        # fields = ['id', 'status', 'payment_method', 'products']
        fields = ['id', 'user', 'products', 'status', 'payment_method', 'created_at', 'updated_at', 'total_quantity', 'order_price']

    def get_total_quantity(self, obj):
        return obj.products.through.objects.filter(order=obj).aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
    
    def get_order_price(self, obj):
        order_products = obj.products.through.objects.filter(order=obj)
        total_price = sum(order_product.product.price * order_product.quantity for order_product in order_products)
        return total_price
    
    def get_products(self, obj):
        order_products = obj.products.through.objects.filter(order=obj)
        product_data = []
        for order_product in order_products:
            product = order_product.product
            quantity = order_product.quantity
            images = product.images.all()
            image_urls = [image.image.url for image in images]
            product_data.append({
                'id': product.id,
                'name': product.name,
                'images': image_urls,
                'description': product.description,
                'price': product.price,
                'quantity': quantity,
                'Totalprice':product.price * quantity,
            })
        return product_data

# serializer = GetOrderSerializer(orders, many=True, context={'request': request})
serializer = GetOrderSerializer(orders ,many=True, context={'request': Request})
