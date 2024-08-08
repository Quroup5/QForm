from rest_framework import serializers
from .models import Form


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
