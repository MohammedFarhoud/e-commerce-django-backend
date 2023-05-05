from django.forms import ValidationError
from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from products.models import Product
import users
from .models import Wishlist
from .serializers import WishlistSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny ,IsAuthenticated
from rest_framework import serializers


class WishlistList(generics.ListCreateAPIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    print('test1')

    def perform_create(self, serializer):
        # if self.request.user.is_authenticated:
            # user = self.request.data.get('user')
            user = self.request.user
            # print(user)
            # if not user.is_authenticated:
                # raise PermissionDenied(detail="You must be logged in to add to your wishlist.")
            
            
            product_id=self.request.data.get('product')
            existing_wishlist = Wishlist.objects.filter(user=user).first()
            # print(existing_wishlist)
            # print(product_id)
            # print(existing_wishlist.product)
            # my_wishlist = Wishlist.objects.get(id=1)
            # print(my_wishlist.product.all())
            print(existing_wishlist)

            if existing_wishlist:
                # products = existing_wishlist.product.all()
                is_in_wishlist = existing_wishlist.product.filter(id=product_id).exists()
                print(is_in_wishlist)
                if is_in_wishlist:
                    raise serializers.ValidationError('product already exists in wishlist')
                else:
                    product = get_object_or_404(Product, id=product_id)
                    existing_wishlist.product.add(product)
                    # serializer.instance = existing_wishlist
                    # valdata date 
                    # serializer.save()
                    existing_wishlist.save()
                    print('product added to existing wishlist')
            else:
                product = get_object_or_404(Product, id=product_id)
                new_wishlist = Wishlist.objects.create(user=user)
                new_wishlist.product.add(product)
                # serializer.instance = new_wishlist
                # serializer.save()
                new_wishlist.save()
                print('product added to new wishlist')



class WishlistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer


class UserWishlistList(generics.ListAPIView):
    serializer_class = WishlistSerializer

    def get_queryset(self):
        # user_id = self.kwargs['user_id']
        permission_classes = [IsAuthenticated]
        user= self.request.user
        if not user.is_authenticated:
            raise PermissionDenied(detail="You must be logged in to add to your wishlist.")
        user_id = self.request.user.id
        return Wishlist.objects.filter(user_id=user_id)
    

class WishlistItemDelete(generics.DestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    lookup_field = 'id'
    # permission_classes = [IsAuthenticated]
# class WishlistItemDelete(generics.DestroyAPIView):
#         product_id = kwargs['product']
#         user = request.user
#         cart = get_object_or_404(Cart, user=user)
#         product = get_object_or_404(Product, id=product_id)
#         cart_product = get_object_or_404(CartProduct, cart=cart, product=product)
#         cart_product.delete()
#         return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)