from http.client import NOT_FOUND
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cart.models import Cart
from orders.models import PaymentHistory
from users.models import CustomUser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from orders.models import Order, OrderProduct
from orders.serializers import  PostOrderSerializer
from rest_framework import status
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import NotFound



class PaymentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Retrieve the user's cart
        user = self.request.user
        # cart = user.cart
        # cart = request.user.cart
        
        try:
            cart = user.cart
        except Cart.DoesNotExist:
            raise NotFound("Cart not found")
        except CustomUser.DoesNotExist:
            raise NotFound("User not found")
    
        total_price = sum([cart_product.quantity * cart_product.product.price for cart_product in cart.cartproduct_set.all()])

        print(total_price)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
              'price_data': {
                'currency': 'usd',
                'unit_amount': int(total_price * 100),
               'product_data': {
                  'name': 'Your purchase',
                },
              },
              'quantity': 1,
            }],
            mode='payment',
            # success_url=settings.SITE_URL + '/?/success=true',
            success_url=settings.SITE_URL + '/orders',
            # cancel_url=settings.SITE_URL + '?/canceled=true',
            cancel_url=settings.SITE_URL + '/cart',
            metadata={'user_id': request.user.id}
        )
        for cart_product in cart.cartproduct_set.all():
            PaymentHistory.objects.create(
                user=request.user, 
                product=cart_product.product, 
                payment_status=False
            )
            


        return JsonResponse({'sessionId': session.url})

    def put(self, request):
        intent_id = request.data.get('intent_id')
        status = request.data.get('status')

        intent = stripe.PaymentIntent.retrieve(intent_id)

        if status == 'succeeded':
            user_id = intent.metadata['user_id']
            user = CustomUser.objects.get(id=user_id)
            cart = user.cart


stripe.api_key = 'sk_test_51N4C2MCnAe4mWFw2TKo8V3gkpZAfU7YE7oJF0MAJUZakxSOjm6jXC01q2knSLXfNI0moAvwoSF9Vhm9setmKAqJ400kB90PKWO'

@csrf_exempt
def my_webhook_view(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header,  settings.STRIPE_SECRET_WEBHOOK
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

      # Handle the checkout.session.completed event
  if event['type'] == 'checkout.session.completed':
    # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
    session = stripe.checkout.Session.retrieve(
      event['data']['object']['id'],
      expand=['line_items'],
    )
    
    print(session)
    customer_email=session['customer_details']['email']
    # prod_id=session['metadata']['product_id']
    # product=Product.objects.get(id=prod_id)
    #sending confimation mail
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        intent = event['data']['object']
        user_id = intent['metadata']['user_id']
        user = CustomUser.objects.get(id=user_id)
        cart = user.cart
        cart_products = cart.cartproduct_set.all()
        order_data = {
            'user': user_id,
            'payment_method': 'visa',
        }
        # customer_email=session['customer_details']['email']
        # send_mail(
        #     subject="payment sucessful",
        #     message=f"thank for your purchase your order is ready.",
        #     recipient_list=[customer_email],
        #     from_email="mahmoudawd54@gmail.com"
        # )
        serializer = PostOrderSerializer(data=order_data)
        if serializer.is_valid():
            order = serializer.save()
            for cart_product in cart_products:
                OrderProduct.objects.create(order=order, product=cart_product.product, quantity=cart_product.quantity)
                cart_product.product.quantity -= cart_product.quantity
                cart_product.product.save()
                PaymentHistory.objects.create(user=user, product=cart_product.product, payment_status=True)
            cart.delete()
            print("Cart deleted succesc" )
            return HttpResponse({'message': 'Order added successfully', 'order': serializer.data}, status=status.HTTP_201_CREATED)
        return HttpResponse({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return HttpResponse(status=200) 
