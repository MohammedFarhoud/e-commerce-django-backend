from django.contrib import admin

from orders.models import Order, OrderProduct
from products.models import Product

class ProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = ('user', 'status')

admin.site.register(Order, OrderAdmin)
