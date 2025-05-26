from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from lms.models import Course
from .models import Payment
from .serializers import (PaymentRequestSerializer,
                          PaymentResponseSerializer)
from .services import (
    create_stripe_product,
    create_stripe_price,
    create_checkout_session,
)
from drf_yasg.utils import swagger_auto_schema

class CheckoutSessionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=PaymentRequestSerializer,
        responses={
            201: PaymentResponseSerializer,
            400: 'Bad Request',
            404: 'Course not found',
        }
    )
    def post(self, request):
        serializer = PaymentRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course = get_object_or_404(Course,pk=serializer.validated_data['course_id'])
        prod = create_stripe_product(course)
        price = create_stripe_price(course, prod.id)
        sess = create_checkout_session(
            price_id=price.id,
            success_url=serializer.validated_data['success_url'],
            cancel_url=serializer.validated_data['cancel_url'],
        )
        Payment.objects.create(
            user=request.user,
            course=course,
            stripe_product_id=prod.id,
            stripe_price_id=price.id,
            stripe_session_id=sess.id,
            session_url=sess.url,
            status=sess.status,
        )
        out = PaymentResponseSerializer({
            'session_id': sess.id,
            'session_url': sess.url,
        })
        return Response(out.data, status=status.HTTP_201_CREATED)
