
from rest_framework import serializers
from .models import Category,Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id', 'name']
        
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    
    class Meta:
        model=Product
        fields = ['id', 'name', 'description', 'image', 'price', 'quantity', 'category']
