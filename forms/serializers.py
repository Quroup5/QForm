from rest_framework import serializers
from .models import Form, Question


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        exclude = ['user']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
