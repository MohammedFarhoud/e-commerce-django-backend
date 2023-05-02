from django.contrib import admin

from orders.models import Order, OrderProduct
from products.models import Product

class ProductInline(admin.TabularInline ,admin.StackedInline):
    model = OrderProduct
    extra = 1
    verbose_name_plural = 'Products'
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = ('get_order_number', 'user', 'status')
    
    def get_order_number(self, obj):
        return f"Order {obj.pk}"
    get_order_number.short_description = 'Order Number'

admin.site.register(Order, OrderAdmin)

    
    
