from django.contrib import admin
from products.models import Product, Category, Image

from django.utils.html import mark_safe


# def image_display(self, obj):
#     return '<img src="{Category.image}" width="50" height="50" />'.format(obj.image.url)  # Replace 'image' with the actual field name in your Category model
    
# image_display.allow_tags = True
# image_display.short_description = 'Image'  # Set the column header name in the admin panel‏

class ProductInline(admin.TabularInline ,admin.StackedInline):
    model = Image
    extra = 1
    verbose_name_plural = 'Images'
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = ('id','name','category','price','quantity',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    

admin.site.register(Product, ProductAdmin)
admin.site.register(Category,CategoryAdmin)
