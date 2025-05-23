from django.urls import path
from .views import CheckoutSessionAPIView

urlpatterns = [
    path('checkout/', CheckoutSessionAPIView.as_view(),
         name='stripe-checkout'),
]