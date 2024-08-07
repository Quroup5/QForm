from rest_framework import serializers

from forms.models import Form


class FormViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        exclude = ['password']


class FormCreateViewSetSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=3, max_length=100)
    password = serializers.CharField(min_length=3, required=False)

    class Meta:
        model = Form
        fields = ['title', 'password']


class FormUpdateViewSetSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=3, max_length=100, required=False)
    password = serializers.CharField(min_length=3, required=False)

    class Meta:
        model = Form
        fields = ['title', 'password']
