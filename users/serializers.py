from rest_framework import serializers
from .models import User


class UserSerializer(
    serializers.ModelSerializer):  # TODO: Check https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, required=True)
    password = serializers.CharField(min_length=6, required=True)
    email = serializers.EmailField(min_length=4, required=True)
