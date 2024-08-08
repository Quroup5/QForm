from rest_framework import serializers
from .models import Form


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        exclude = ['user']
        extra_kwargs = {
            'password': {'write_only': True}
        }
