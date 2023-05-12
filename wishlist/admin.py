from django.contrib import admin
from stripe import Product

from wishlist.models import Wishlist
class WishlistAdmin(admin.ModelAdmin):
    inlines = []
    list_display = ('get_Wishlist_number', 'user')
    
    def get_Wishlist_number(self, obj):
        return f"Wishlist {obj.pk}"
    get_Wishlist_number.short_description = 'Wishlist Number'

admin.site.register(Wishlist,WishlistAdmin)
