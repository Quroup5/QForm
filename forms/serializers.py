from rest_framework import serializers
from .models import Form, Category, Process


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        exclude = ['user']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']
        extra_kwargs = {
            'user': {'read_only': True}
        }
