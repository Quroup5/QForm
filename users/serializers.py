from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ['password']


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=3, required=True)
    password = serializers.CharField(min_length=6, required=True)
    email = serializers.EmailField(min_length=4, required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(min_length=2, required=False)
    last_name = serializers.CharField(min_length=2, required=False)
    email = serializers.EmailField(min_length=4, required=False)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']


class OtpSerializerRequest(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True)


class OtpSerializerVerification(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True)
    password = serializers.CharField(min_length=6, required=True)
    otp = serializers.CharField(min_length=4, max_length=4, required=True)
