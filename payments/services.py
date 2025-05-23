import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(course):
    return stripe.Product.create(name=course.title)

def create_stripe_price(course, product_id):
    return stripe.Price.create(
        product=product_id,
        unit_amount=int(course.price * 100),
        currency="usd",
    )

def create_checkout_session(price_id, success_url, cancel_url):
    return stripe.checkout.Session.create(
        success_url=success_url,
        cancel_url=cancel_url,
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
