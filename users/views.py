from django.shortcuts import render
from users.serializers import Address, CustomUser
from rest_framework import generics, status
from users.serializers import AddressSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        
class AddressRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(user = self.request.user)
    
    def get_object(self):
        querysey = self.get_queryset()
        user = self.request.user
        id = self.kwargs['id']
        address_object = get_object_or_404(querysey, id = id)
        if address_object.user != user:
            self.permission_denied(self.request)
        return address_object

class Registeration(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)