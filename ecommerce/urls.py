from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from products.views  import CategoryViewSet, ProductViewSet ,ProductListByCategory ,ProductList
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from wishlist.views import WishlistList, WishlistDetail ,UserWishlistList ,WishlistItemDelete
# from orders.views import PaymentView 
# from orders.views import CreateCheckOutSession ,stripe_webhook_view
from orders.views import PaymentView ,create_payment_intent ,process_payment

router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    
    
    
    path('category/<int:category_id>/products', ProductListByCategory.as_view(), name='product_list_by_category'),
    # path('productserach/', ProductList.as_view(), name='product_list'),
    # path('productsearch/', ProductViewSet.as_view({'get': 'list'}), name='product_search'),

    path('wishlist', WishlistList.as_view(), name='wishlist-list'),
    path('wishlist/<int:pk>/', WishlistDetail.as_view(), name='wishlist-detail'),
    # path('user/wishlist/<int:user_id>/', UserWishlistList.as_view(), name='user-wishlist-list'),
    path('user/wishlist', UserWishlistList.as_view(), name='user-wishlist-list'),
    path('wishlist/product/<int:id>/', WishlistItemDelete.as_view(), name='remove-from-wishlist'),
    
    # path('api/payments/create-payment-intent/',create_payment_intent),
    path('payment/', PaymentView.as_view(), name='payment'),
    
    path('api/payments/create-payment-intent/', create_payment_intent, name='create_payment_intent'),
    path('api/payments/', process_payment, name='process_payment'),


    # path('create_checkout_session/', CreateCheckOutSession, name='create_checkout_session'),
    # path('stripe_webhook/', stripe_webhook_view, name='stripe_webhook'),
    # path('create-checkout-session/', views.CreateCheckOutSession, name='create_checkout_session'),

    
    
    path('auth/', include('users.urls')),
    path('cart/', include('cart.urls')),
 ]
