from django.shortcuts import redirect, render
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cart.models import Cart
from orders.models import PaymentHistory
from products.models import Product
from django.http import HttpResponse
import json
from rest_framework.decorators import api_view
from django.core.mail import send_mail

from users.models import CustomUser
from django.views.decorators.csrf import ensure_csrf_cookie

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from cart.models import Cart
from orders.models import Order, OrderProduct
from orders.serializers import GetOrderSerializer, PostOrderSerializer
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer




class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        payment_method = request.data.get('payment_method')
        cart_products = cart.cartproduct_set.all()
        order_data = {
            'user': request.user.id,
            'payment_method': payment_method,
        }
        serializer = PostOrderSerializer(data=order_data)
        if serializer.is_valid():
            order = serializer.save()
            for cart_product in cart_products:
                OrderProduct.objects.create(order=order, product=cart_product.product, quantity=cart_product.quantity)
            cart.delete()
            return Response({'message': 'Order added successfully', 'order': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
    def put(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        if order.status == 'PENDING':
            order.status = 'CANCELLED'
            order.save()
            return Response({'message': 'Order cancelled successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Order status should be pending to cancel'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        if not orders:
            return Response({'error': 'No orders found for the user'}, status=status.HTTP_404_NOT_FOUND)
        serializer = GetOrderSerializer(orders, many=True)
        return Response({'message': 'Orders found', 'orders': serializer.data}, status=status.HTTP_200_OK)

# @api_view(['POST'])
# @csrf_exempt
# def stripe_webhook_view(request):
#     # Retrieve the event from Stripe
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#         )
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse(status=400)

#     # Handle the event
#     if event['type'] == 'payment_intent.succeeded':
#         intent = event['data']['object']
#         user_id = intent['metadata']['user_id']
#         user = CustomUser.objects.get(id=user_id)
#         cart = user.cart
#         cart_products = cart.cartproduct_set.all()
#         order_data = {
#             'user': user_id,
#             'payment_method': intent['payment_method'],
#         }
#         serializer = PostOrderSerializer(data=order_data)
#         if serializer.is_valid():
#             order = serializer.save()
#             for cart_product in cart_products:
#                 OrderProduct.objects.create(order=order, product=cart_product.product, quantity=cart_product.quantity)
#                 PaymentHistory.objects.create(user=user, product=cart_product.product, payment_status=True)
#             cart.delete()
#             return HttpResponse({'message': 'Order added successfully', 'order': serializer.data}, status=status.HTTP_201_CREATED)
#         return HttpResponse({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#     # Default response for unhandled events
#     return HttpResponse(status=200)

class StripeCheckoutView(APIView):
    def post(self, request):
        try:
            cart = request.user.cart
            total_price = sum([cart_product.quantity * cart_product.product.price for cart_product in cart.cartproduct_set.all()])

            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(total_price * 100),
                            'product_data': {
                                'name': 'Cart Total',
                            },
                        },
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card',],
                mode='payment',
                success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/?canceled=true',
            )

            return redirect(checkout_session.url)
        except:
            return Response(
                {'error': 'Something went wrong when creating stripe checkout session'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PaymentView(APIView):
    def post(self, request):
        # Retrieve the user's cart
        cart = request.user.cart

        # Calculate the total price of the products in the cart
        total_price = sum([cart_product.quantity * cart_product.product.price for cart_product in cart.cartproduct_set.all()])

        print(total_price)
        # Create a new Stripe Checkout session for the total amount
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
              'quantity': 2,
            }],
            mode='payment',
            success_url=settings.SITE_URL + '?/success=true',
            cancel_url=settings.SITE_URL + '?/canceled=true',
            metadata={'user_id': request.user.id}
        )
        for cart_product in cart.cartproduct_set.all():
            PaymentHistory.objects.create(
                user=request.user, 
                product=cart_product.product, 
                payment_status=False
            )
            

        # return Response({'session_id': session.id}, status=status.HTTP_200_OK)
        # return redirect(session.url, code=303)
        # print(session)
        # return JsonResponse({'sessionId': session['id']})
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
                PaymentHistory.objects.create(user=user, product=cart_product.product, payment_status=True)
            # cart.delete()
            return HttpResponse({'message': 'Order added successfully', 'order': serializer.data}, status=status.HTTP_201_CREATED)
        return HttpResponse({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return HttpResponse(status=200)


@csrf_exempt
def create_payment_intent(request):
    if request.method == "POST":
        cart_id = request.POST.get("cart_id")

        intent = stripe.PaymentIntent.create(
            amount=int(10*10), 
            currency="usd",
            metadata={"cart_id": cart_id}
        )

        return JsonResponse({
            "client_secret": intent.client_secret,
            "amount": intent.amount
        })
    else:
        return JsonResponse({"error": "Invalid request method"})
    
@csrf_exempt
@api_view(['POST'])
def process_payment(request):
    stripe.api_key = 'your_stripe_secret_key'
    data = request.data
    amount = data['amount']
    payment_method_id = data['payment_method_id']

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            payment_method=payment_method_id,
            confirmation_method='manual',
            confirm=True
        )
        return Response({'succeeded': True})
    except Exception as e:
        return Response({'error': str(e)})

