from django.urls import path
from orders.views import OrderView

urlpatterns = [
    path('', OrderView.as_view(), name='order'),
    path('<int:order_id>/', OrderView.as_view(), name='cancel-order'),
]