from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from products.views  import CategoryViewSet, ProductViewSet ,ProductListByCategory ,ProductList
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from wishlist.views import WishlistList, WishlistDetail ,UserWishlistList ,WishlistItemDelete


router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    
    
    
    path('category/<int:category_id>/products', ProductListByCategory.as_view(), name='product_list_by_category'),
    path('productserach/', ProductList.as_view(), name='product_list'),
    path('wishlist', WishlistList.as_view(), name='wishlist-list'),
    path('wishlist/<int:pk>/', WishlistDetail.as_view(), name='wishlist-detail'),
    # path('user/wishlist/<int:user_id>/', UserWishlistList.as_view(), name='user-wishlist-list'),
    path('user/wishlist', UserWishlistList.as_view(), name='user-wishlist-list'),
    path('wishlist/delete/<int:id>/', WishlistItemDelete.as_view(), name='remove-from-wishlist'),

    path('auth/', include('users.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
]
