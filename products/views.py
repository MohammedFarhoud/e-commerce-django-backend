from django.shortcuts import render
from rest_framework import viewsets

from products.pagination import ProductPagination

from .models import Category,Product
from .serializers import CategorySerializer,ProductSerializer
from rest_framework.generics import ListAPIView

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend



# class ProductFilter(filters.FilterSet):
#     category_name = filters.CharFilter(field_name='category__name', lookup_expr='iexact')

#     class Meta:
#         model = Product
#         fields = ['category_name']

        
class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['category__name']




class ProductListByCategory(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Product.objects.filter(category__id=category_id)
    
class ProductList(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        search_term = self.request.query_params.get('search', '')
        if search_term:
            return Product.objects.filter(name__icontains=search_term)
        else:
            return Product.objects.all()