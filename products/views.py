from rest_framework import viewsets
from .models import Category,Product, Image
from .serializers import CategorySerializer, ImageSerializer,ProductSerializer
from products.pagination import ProductPagination
from rest_framework.generics import ListAPIView

class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    
class ImageViewSet(viewsets.ModelViewSet):
    queryset=Image.objects.all()
    serializer_class=ImageSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    pagination_class = ProductPagination
    


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