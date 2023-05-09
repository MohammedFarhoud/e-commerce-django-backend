from django.forms import ValidationError
from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response

from products.models import Product
import users
from wishlist.pagination import WishlistPagination
from .models import Wishlist
from .serializers import WishlistSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny ,IsAuthenticated
from rest_framework import serializers ,status


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
    # pagination_class = WishlistPagination


    def get_queryset(self):
        # user_id = self.kwargs['user_id']
        permission_classes = [IsAuthenticated]
        user= self.request.user
        if not user.is_authenticated:
            raise PermissionDenied(detail="You must be logged in to add to your wishlist.")
        user_id = self.request.user.id
        return Wishlist.objects.filter(user_id=user_id)
    


class WishlistItemDelete(APIView):
    def delete(self, request, id):
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            product = Product.objects.get(id=id)
            wishlist.product.remove(product)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Wishlist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            return Response(data={'error': 'Product not found in wishlist.'}, status=status.HTTP_400_BAD_REQUEST)

