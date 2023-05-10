from rest_framework import serializers
from cart.models import Cart, CartProduct
from cart.pagination import CartProductPagination
from products.serializers import ProductSerializer
from django.core.validators import MinValueValidator

class AddToCartSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(validators=[MinValueValidator(1)], default=1)

    class Meta:
        model = CartProduct
        fields = ['product', 'quantity']
        
    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']
        user = self.context.get('user')
        
        cart, created = Cart.objects.get_or_create(user=user)
        cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_product.quantity += quantity
        else:
            cart_product.quantity = quantity

        cart_product.save()
            
        return cart_product
    
class UpdateCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartProduct
        fields = ['product', 'quantity']
        
    def update(self, instance ,validated_data):
        action = self.context.get('action')
        if action not in ('INCREASE', 'DECREASE'):
            raise serializers.ValidationError({'error': "Action can only be 'INCREASE' or 'DECREASE'"})
        
        if action == 'INCREASE':
            instance.quantity += 1
        elif action == 'DECREASE' and instance.quantity > 0:
            instance.quantity -= 1
        instance.save()
        
        if instance.quantity == 0:
            instance.delete()
            
        return instance

class CartSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, instance):
            return instance.calculate_total_price()
        
    def get_products(self, instance):
        cart_products = instance.cartproduct_set.all()
        request = self.context.get('request')
        paginator = CartProductPagination()
        paginated_products = paginator.paginate_queryset(cart_products, request)

        products = []
        for cart_product in paginated_products:
            products.append({
                'id': cart_product.product.id,
                'name': cart_product.product.name,
                'description': cart_product.product.description,
                'image': cart_product.product.image.url,
                'price': cart_product.product.price,
                'category': cart_product.product.category.name,
                'quantity': cart_product.quantity,
            })
        return products
    
    class Meta:
        model = Cart
        fields = ['id', 'products', 'total_price']
