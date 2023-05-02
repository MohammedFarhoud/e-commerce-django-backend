from django.core.exceptions import ValidationError
from rest_framework import serializers
from users.models import CustomUser, Address
        
class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address,
        fields = '__all__'
    
class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)

    class Meta:
        model = CustomUser,
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }
    
    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)
    
    def validate(self, data):
        if CustomUser.objects.filter(email=data['email']).exists():
            raise ValidationError('This email is already registered.')
        
        if CustomUser.objects.filter(phone=data['phone']).exists():
            raise ValidationError('This phone number is already registered.')
        
        if data['password'] != data['confirm_password']:
            raise ValidationError('Passwords do not match.')
        
        return data