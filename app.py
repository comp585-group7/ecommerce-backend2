import os
import stripe
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set your Stripe secret key. For local testing, you can hardcode it here, but never do this for production.
# In production, you'll use an environment variable.
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_51OQD9DLQmZaxf1veBWMQ53wvnnPGtfYeszUcJuOMmwHYsMYx2vNah8s97P4GzRfsyGKJou5ZvRFCpskX0A62h0pP00PdT6Q1sW')

@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        data = request.get_json()
        amount = data['amount']     # amount in smallest currency unit (cents if USD)
        currency = data['currency'] # e.g. "usd"

        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
        )

        return jsonify({'clientSecret': payment_intent.client_secret})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=4242, debug=True)
