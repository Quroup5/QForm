from django.contrib.auth import get_user_model
from rest_framework import serializers

from forms.models import Form


class CreateFormSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=100)
    password = serializers.CharField(min_length=3, required=False)


class UpdateFormSerializer(serializers.Serializer):
    form_id = serializers.IntegerField(required=True)
    title = serializers.CharField(min_length=3, max_length=100, required=False)
    password = serializers.CharField(min_length=3, required=False)
    category = serializers.CharField(min_length=3, max_length=255, required=False)
