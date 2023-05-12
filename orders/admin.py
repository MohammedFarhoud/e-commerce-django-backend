from django.contrib import admin

from orders.models import Order, OrderProduct
from products.models import Product

class ProductInline(admin.TabularInline ,admin.StackedInline):
    model = OrderProduct
    extra = 1
    verbose_name_plural = 'Products'
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = ('id','user', 'status','payment_method','created_at','updated_at',)
    


admin.site.register(Order, OrderAdmin)

    
    
