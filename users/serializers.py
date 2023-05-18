from django.core.exceptions import ValidationError
from rest_framework import serializers
from users.models import CustomUser, Address, ContactUs
from cloudinary.models import CloudinaryField
from django.contrib.auth.hashers import make_password

class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = '__all__'
        
    def update(self, instance, validated_data):
        instance.street = validated_data.get('street', instance.street)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.country = validated_data.get('country', instance.country)
        instance.save()
        return instance
    
class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, required=False)

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }
    
    def create(self, validated_data):
        validated_data.pop('groups')
        validated_data.pop('user_permissions')
        validated_data['is_active'] = True
        return CustomUser.objects.create_user(**validated_data)
    
    def validate(self, data):
        if CustomUser.objects.filter(email=data['email']).exists():
            raise ValidationError('This email is already registered.')
        
        if CustomUser.objects.filter(phone=data['phone']).exists():
            raise ValidationError('This phone number is already registered.')
        
        if data['password'] != data['confirm_password']:
            raise ValidationError('Passwords do not match.')
        
        return data
class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    phone=serializers.CharField(required=False)
    image=CloudinaryField()
    password = serializers.CharField(required=False, write_only=True)
    confirm_password = serializers.CharField(required=False, write_only=True)
    # addresses = AddressSerializer(many=True)


    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name','phone','image','password','confirm_password' , 'addresses']
        
    def validate(self, attrs):
        if not any(attrs.values()):
            print('upadta users')
            raise serializers.ValidationError("At least one field must be updated")

        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if not password or not confirm_password or password != confirm_password:
            print('upadta sssss')
            # raise serializers.ValidationError
        return attrs
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        confirm_password = validated_data.pop('confirm_password', None)
        addresses_data = validated_data.pop('addresses',[])
        if password and confirm_password:
            validated_data['password'] = make_password(password)
            validated_data['confirm_password'] = make_password(confirm_password)
        instance = super().update(instance, validated_data)
        print('44444444444444')
        for address_data in addresses_data:
            address_id = address_data.get('id', None)
            if address_id:
                try:
                    address = Address.objects.get(id=address_id, user=instance)
                    address_serializer = AddressSerializer(address, data=address_data)
                    if address_serializer.is_valid():
                        address_serializer.save()
                    else:
                        raise serializers.ValidationError(address_serializer.errors)
                except Address.DoesNotExist:
                    raise serializers.ValidationError(f"Address with id {address_id} does not exist.")
            else:
                address_serializer = AddressSerializer(data=address_data)
                if address_serializer.is_valid():
                    address_serializer.save(user=instance)
                else:
                    raise serializers.ValidationError(address_serializer.errors)


        return instance

class ContactUsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ContactUs
        fields = '__all__'