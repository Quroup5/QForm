from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Form, Process, FormProcess, Question
from .serializers import FormSerializer, ProcessSerializer, FormProcessSerializer, QuestionSerializer, \
    FormProcessDisplaySerializer, FormDisplaySerializer


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
