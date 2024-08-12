from rest_framework import serializers
from .models import Form, Process, Question, Category, Answer, FormProcess
from django.contrib.auth.hashers import check_password


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        exclude = ['user', 'visitor_count', 'answer_count']
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


class AnswerSerializer(serializers.ModelSerializer):
    form = serializers.PrimaryKeyRelatedField(queryset=Form.objects.all())
    process = serializers.PrimaryKeyRelatedField(queryset=Process.objects.all(), required=False)
    responder_nickname = serializers.CharField(max_length=255)  # New field
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Answer
        fields = ['form', 'process', 'answer', 'responder_nickname', 'password']

    def validate(self, data):
        form = data.get('form')
        answers = data.get('answer')
        password = data.get('password')
        process = data.get('process')
        responder_nickname = data.get('responder_nickname')

        # Ensure the form exists
        if not form:
            raise serializers.ValidationError({"form": "Form does not exist."})

        if form.is_private:
            if not password:
                raise serializers.ValidationError({"password": "Form is password protected."})
            if not check_password(password, form.password):
                raise serializers.ValidationError({"password": "Incorrect password."})

        # Validate responder_nickname
        if not responder_nickname:
            raise serializers.ValidationError({"responder_nickname": "Responder nickname is required."})

        # If a process is provided, ensure the answer order is correct if the process is linear
        if process:
            form_process = FormProcess.objects.filter(process=process, form=form).first()

            if not form_process:
                raise serializers.ValidationError({"process": "Form does not belong to the provided process."})

            if process.type == Process.LINEAR:
                # Ensure that the previous forms in the process have been completed
                previous_forms = FormProcess.objects.filter(
                    process=process,
                    order__lt=form_process.order
                ).values_list('form_id', flat=True)

                missing_answers = set(previous_forms) - set(Answer.objects.filter(
                    process=process,
                    form_id__in=previous_forms,
                    responder_nickname=responder_nickname
                ).values_list('form_id', flat=True))

                if missing_answers:
                    raise serializers.ValidationError({
                        "process": f"You must respond to previous forms in the process before this one. Missing forms: {missing_answers}"
                    })

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

        data.pop('password', None)  # Remove password from the data before returning
        return data


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        exclude = ['user', 'visitor_count', 'answer_count']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class FormProcessSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = FormProcess
        fields = ['form', 'process', 'order']

    def validate(self, data):
        process = data.get('process')
        order = data.get('order')

        if process.type == process.LINEAR and order is None:
            raise serializers.ValidationError({'order': 'This field is required. Process is linear.'})

        return data


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
