from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Form, Process, FormProcess, Question, Category, Answer
from .serializers import FormSerializer, ProcessSerializer, FormProcessSerializer, QuestionSerializer, \
    FormProcessDisplaySerializer, FormDisplaySerializer, CategorySerializer, AnswerSerializer


class IsFormOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsQuestionOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.form.user == request.user

    def has_permission(self, request, view):
        if view.action == 'create':
            form_pk = request.data.get('form')
            if form_pk:
                try:
                    form = Form.objects.get(pk=form_pk)
                    return form.user == request.user
                except Form.DoesNotExist:
                    return False
        return True


class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [permissions.IsAuthenticated, IsFormOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Form.objects.filter(user=self.request.user)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated, IsQuestionOwner]

    def get_queryset(self):
        return Question.objects.filter(form__user=self.request.user)


class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    permission_classes = [permissions.IsAuthenticated, IsFormOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Process.objects.filter(user=self.request.user)


class IsFormProcessOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.form.user == request.user and obj.process.user == request.user


class FormProcessViewSet(viewsets.ModelViewSet):
    queryset = FormProcess.objects.all()
    serializer_class = FormProcessSerializer
    permission_classes = [permissions.IsAuthenticated, IsFormProcessOwner]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        process = serializer.validated_data.get("process")
        form = serializer.validated_data.get("form")

        if form.user != self.request.user or process.user != self.request.user:
            return Response(data={'msg': 'Select correct form or process'},
                            status=status.HTTP_401_UNAUTHORIZED)

        return super().create(request, *args, **kwargs)


class DisplayProcesView(APIView):
    serializer_class = FormProcessDisplaySerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        target_process = serializer.validated_data.get('process')

        query = get_list_or_404(FormProcess.objects.filter(process=target_process).order_by("order"))
        data = {}
        for form_number, form_process in enumerate(query):
            form_process.form.visitor_count += 1
            form_process.form.save()
            questions = Question.objects.filter(form=form_process.form)
            data[f'f{form_number + 1}'] = QuestionSerializer(questions, many=True).data

        target_process.visitor_count += 1
        target_process.save()
        return Response(data=data, status=status.HTTP_200_OK)


class DisplayFormView(APIView):
    serializer_class = FormDisplaySerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        target_form = get_object_or_404(Form, id=serializer.validated_data.get('id'))
        target_form.visitor_count += 1
        target_form.save()
        data = {}
        questions = Question.objects.filter(form=target_form)
        data[f'f1'] = QuestionSerializer(questions, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsFormOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Save the answer first to get the instance
        answer = serializer.save()

        # Increment the answer_count for the form
        form = answer.form
        form.answer_count += 1
        form.save()

        # Check if the process needs to be updated
        process = answer.process
        if process:
            self.update_process_answer_count(process, answer.responder_nickname)

    def update_process_answer_count(self, process, responder_nickname):
        """
        Increment the answer_count for the process if all forms have been answered by the same responder.
        """
        form_ids_in_process = FormProcess.objects.filter(process=process).values_list('form_id', flat=True)
        answered_form_ids = Answer.objects.filter(
            process=process,
            responder_nickname=responder_nickname
        ).values_list('form_id', flat=True).distinct()

        if set(form_ids_in_process) == set(answered_form_ids):
            process.answer_count += 1
            process.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if the form is part of a process and if it's being submitted in the correct order
        process = serializer.validated_data.get('process')
        form = serializer.validated_data.get('form')
        responder_nickname = serializer.validated_data.get('responder_nickname')

        if process and process.type == Process.LINEAR:
            # Ensure that answers are submitted in the correct order
            form_process = FormProcess.objects.filter(process=process, form=form).first()

            previous_answers = Answer.objects.filter(
                process=process,
                form__in=FormProcess.objects.filter(process=process, order__lt=form_process.order).values('form'),
                responder_nickname=responder_nickname
            )

            if previous_answers.count() < form_process.order - 1:
                return Response(
                    {"detail": "You must complete previous forms in the process before submitting this one."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Save the answer and update answer_count
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


