from rest_framework.views import APIView
import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response


stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET

FRONTEND_CHECKOUT_SUCCESS_URL = settings.CHECKOUT_SUCCESS_URL
FRONTEND_CHECKOUT_FAILED_URL = settings.CHECKOUT_FAILED_URL

class CreateCheckoutSession(APIView):
  def post(self, request):
    dataDict = dict(request.data)
    price = dataDict['price']
    product_name = dataDict['product_name']
    try:
      checkout_session = stripe.checkout.Session.create(
        line_items =[{
        'price_data' :{
          'currency' : 'usd',  
            'product_data': {
              'name': product_name,
            },
          'unit_amount': price
        },
        'quantity' : 1
      }],
        mode= 'payment',
        success_url= FRONTEND_CHECKOUT_SUCCESS_URL,
        cancel_url= FRONTEND_CHECKOUT_FAILED_URL,
        )

      return Response(data={'url': checkout_session.url}, status=200)
    except Exception as ex:
      print(ex)
      return Response(data={'error': str(ex)}, status=400)

class WebHook(APIView):
  def post(self , request):
    event = None
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
      event = stripe.Webhook.construct_event(
        payload ,sig_header , webhook_secret
        )
    except ValueError as err:
        # Invalid payload
        raise err
    except stripe.error.SignatureVerificationError as err:
        # Invalid signature
        raise err

    # Handle the event
    if event.type == 'payment_intent.succeeded':
      payment_intent = event.data.object 
      print("--------payment_intent and I am webhook and I have triggered after a successful payment ---------->" , payment_intent)
    
    else:
      print('Unhandled event type {}'.format(event.type))

    return JsonResponse(success=True, safe=False)