from flask import Flask, jsonify, request
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Stripe setup
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
YOUR_DOMAIN = "http://localhost:8501"  # Your Streamlit app

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Moral Mirror Donation',
                    },
                    'unit_amount': 500,  # $5 donation
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=YOUR_DOMAIN + '/thankyou',
            cancel_url=YOUR_DOMAIN + '/cancelled',
        )
        return jsonify({'id': session.id, 'url': session.url})
    except Exception as e:
        return jsonify(error=str(e)), 403

if __name__ == '__main__':
    app.run(port=4242)
