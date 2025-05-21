from rest_framework import serializers
from .models import Payment
from django.contrib.auth import get_user_model

User = get_user_model()

class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    paid_course = serializers.StringRelatedField()
    paid_lesson = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

