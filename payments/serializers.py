from rest_framework import serializers

class PaymentRequestSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    success_url = serializers.URLField()
    cancel_url = serializers.URLField()

class PaymentResponseSerializer(serializers.Serializer):
    session_id = serializers.CharField()
    session_url = serializers.URLField()
