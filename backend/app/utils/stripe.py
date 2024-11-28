# app/utils/stripe.py
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

class StripeService:
    @staticmethod
    def create_payment_intent(amount, currency='jpy'):
        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency
            )
            return {
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id
            }
        except Exception as e:
            raise Exception(f"Failed to create payment intent: {str(e)}")

    @staticmethod
    def confirm_payment(payment_intent_id):
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return payment_intent.status == 'succeeded'
        except Exception as e:
            raise Exception(f"Failed to confirm payment: {str(e)}")