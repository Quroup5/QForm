from rest_framework import serializers
from .models import Form, Process, Question, Category, Response, FormProcess


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        exclude = ['user', 'visitor_count', 'response_count']
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
            # Validate metadata for 'select' type
            if not isinstance(metadata, dict) or "options" not in metadata:
                raise serializers.ValidationError({
                    "metadata": "Metadata for 'select' type must include an 'options' key."
                })
            options = metadata.get("options")
            if not isinstance(options, list) or not all(isinstance(opt, str) for opt in options):
                raise serializers.ValidationError({
                    "metadata": "The 'options' key must be a list of strings."
                })

        elif question_type == Question.CHECKBOX:
            # Validate metadata for 'checkbox' type
            if not isinstance(metadata, dict) or "options" not in metadata:
                raise serializers.ValidationError({
                    "metadata": "Metadata for 'checkbox' type must include an 'options' key."
                })
            options = metadata.get("options")
            if not isinstance(options, list) or not all(isinstance(opt, str) for opt in options):
                raise serializers.ValidationError({
                    "metadata": "The 'options' key must be a list of strings."
                })

        return data


class ResponseSerializer(serializers.ModelSerializer):
    form = serializers.PrimaryKeyRelatedField(queryset=Form.objects.all())

    class Meta:
        model = Response
        fields = ['form', 'answer']

    def validate(self, data):
        form_id = data.get('form').id
        answers = data.get('answer')

        # Ensure the form exists
        try:
            print('********************************************************************')
            print(form_id, answers)
            print('********************************************************************')
            form = Form.objects.get(pk=form_id)
            print('********************************************************************')
            print(data)
            print('********************************************************************')
        except Form.DoesNotExist:
            raise serializers.ValidationError({"form": "Form does not exist."})

        # Validate that all provided answers match the form's questions
        questions = Question.objects.filter(form=form)
        question_map = {q.name: q for q in questions}

        if not isinstance(answers, dict):
            raise serializers.ValidationError({"answer": "Answers must be a dictionary."})

        for question_name, answer in answers.items():
            if question_name not in question_map:
                raise serializers.ValidationError({
                    "answer": f"Invalid question name: {question_name}."
                })

            question = question_map[question_name]
            if question.required and not answer:
                raise serializers.ValidationError({
                    "answer": f"Question '{question_name}' is required."
                })

            if question.type == Question.TEXT and not isinstance(answer, str):
                raise serializers.ValidationError({
                    "answer": f"Answer for question '{question_name}' must be a string."
                })
            elif question.type == Question.SELECT:
                if not isinstance(answer, str):
                    raise serializers.ValidationError({
                        "answer": f"Answer for question '{question_name}' must be a string."
                    })
                if answer not in question.metadata.get("options", []):
                    raise serializers.ValidationError({
                        "answer": f"Invalid option selected for question '{question_name}'."
                    })
            elif question.type == Question.CHECKBOX:
                if not isinstance(answer, list) or not all(isinstance(opt, str) for opt in answer):
                    raise serializers.ValidationError({
                        "answer": f"Answer for question '{question_name}' must be a list of strings."
                    })
                if not all(opt in question.metadata.get("options", []) for opt in answer):
                    raise serializers.ValidationError({
                        "answer": f"Invalid options selected for question '{question_name}'."
                    })

        return data


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        exclude = ['user', 'visitor_count', 'response_count']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class FormProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormProcess
        fields = "__all__"


class FormProcessDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = FormProcess
        fields = ["process"]


class FormDisplaySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Form
        fields = ["id"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']
        extra_kwargs = {
            'user': {'read_only': True}
        }
