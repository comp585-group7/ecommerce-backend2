import os
import stripe
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set your Stripe secret key
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_51OQD9DLQmZaxf1veBWMQ53wvnnPGtfYeszUcJuOMmwHYsMYx2vNah8s97P4GzRfsyGKJou5ZvRFCpskX0A62h0pP00PdT6Q1sW')

@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        data = request.get_json()
        amount = data['amount']     # amount in smallest currency unit (cents)
        currency = data['currency'] # e.g. "usd"

        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
        )

        return jsonify({'clientSecret': payment_intent.client_secret})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.get_json()
        amount = data['amount']     # in smallest currency unit
        currency = data['currency'] # e.g. "usd"

        # Check the referer or other request info to decide which URLs to use
        referer = request.headers.get("Referer", "")

        # Default to the netlify domain
        success_url = 'https://dazzling-tanuki-f69421.netlify.app/#/success'
        cancel_url = 'https://dazzling-tanuki-f69421.netlify.app/#/cancel'

        # If the referer suggests the user is on localhost, use localhost URLs
        if 'localhost:3000' in referer:
            success_url = 'http://localhost:3000/#/success'
            cancel_url = 'http://localhost:3000/#/cancel'

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': 'Your Product',
                    },
                    'unit_amount': amount, # amount is in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )

        return jsonify({'url': session.url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=4242, debug=True)
