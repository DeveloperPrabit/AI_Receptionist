import stripe
import paypalrestsdk
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from .models import Plan, Subscription, PaymentRecord
from .serializers import PlanSerializer, SubscriptionSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

class PlanListView(generics.ListAPIView):
    queryset = Plan.objects.filter(is_active=True)
    serializer_class = PlanSerializer

class CreateStripeCheckoutSessionView(APIView):
    def post(self, request):
        plan_id = request.data.get('plan_id')
        
        if not plan_id:
            return Response({'error': 'Plan ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            plan = Plan.objects.get(id=plan_id)
            
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': plan.name,
                            },
                            'unit_amount': int(plan.price * 100),
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=settings.FRONTEND_URL + '/payment/success/',
                cancel_url=settings.FRONTEND_URL + '/payment/cancel/',
            )
            
            return Response({'sessionId': checkout_session.id})
        except Plan.DoesNotExist:
            return Response({'error': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StripeWebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = 'your-webhook-secret'  # Set in Stripe dashboard
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            return Response({'error': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle the event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            # Fulfill the purchase
            handle_checkout_session(session)
        
        return Response({'status': 'success'})

def handle_checkout_session(session):
    # Implement your logic here
    pass