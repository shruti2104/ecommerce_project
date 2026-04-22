import os

class Config:
    STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY") or "pk_test_..."
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY") or "sk_test_..."