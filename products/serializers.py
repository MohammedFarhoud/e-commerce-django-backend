from rest_framework import serializers
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
    
    class Meta:
        model=Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'category', 'images']