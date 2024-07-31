from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):          # TODO: Check https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
