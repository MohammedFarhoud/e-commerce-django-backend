from django.urls import path
from cart.views import CartView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('delete/<int:product>/', CartView.as_view(), name='remove_from_cart'),
]