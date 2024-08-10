from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import Form, Process, FormProcess, Question
from .serializers import FormSerializer, ProcessSerializer, FormProcessSerializer, QuestionSerializer


class IsFormOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user



class IsQuestionOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.form.user == request.user


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
        """
        Optionally restricts the returned questions to a given form,
        by filtering against a `form_id` query parameter in the URL.
        """
        queryset = Question.objects.all()
        form_id = self.request.query_params.get('form_id')
        if form_id is not None:
            queryset = queryset.filter(form_id=form_id)
        return queryset



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

    #
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    #
    # def get_queryset(self):
    #     return Process.objects.filter(user=self.request.user)
