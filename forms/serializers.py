from rest_framework import serializers
from .models import Form, Process, FormProcess, Question
import re


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

    def validate(self, data):
        """
        Custom validation to ensure metadata conforms to the type's rules.
        """
        question_type = data.get('type')
        metadata = data.get('metadata')

        if question_type == Question.TEXT:
            if metadata:
                raise serializers.ValidationError({"metadata": "Metadata should be empty for type 'text'."})

        elif question_type == Question.SELECT:
            self._validate_dynamic_keys(metadata, 'selectbox', question_type)

        elif question_type == Question.CHECKBOX:
            self._validate_dynamic_keys(metadata, 'checkbox', question_type)

        return data

    @staticmethod
    def _validate_dynamic_keys(metadata, prefix, question_type):
        """
        Helper method to validate metadata keys and structure for dynamic keys.
        """
        if not isinstance(metadata, dict):
            raise serializers.ValidationError(
                {"metadata": f"Metadata should be a dictionary for type '{question_type}'."})

        pattern = re.compile(rf"^{prefix}\d+$")
        for key, value in metadata.items():
            if not pattern.match(key):
                raise serializers.ValidationError({
                    "metadata": f"Keys in metadata must start with '{prefix}' followed by a number for type '{question_type}'."})
            if not isinstance(value, str):
                raise serializers.ValidationError(
                    {"metadata": f"All values in metadata must be strings for type '{question_type}'."})


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        exclude = ['user']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class FormProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormProcess
        fields = "__all__"
