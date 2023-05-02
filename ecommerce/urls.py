
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from products.views  import CategoryViewSet, ProductViewSet ,ProductListByCategory ,ProductList


router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    
    path('category/<int:category_id>/products', ProductListByCategory.as_view(), name='product_list_by_category'),
    path('productserach/', ProductList.as_view(), name='product_list'),


]
