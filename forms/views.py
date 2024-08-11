from rest_framework import viewsets, permissions
from .models import Form, Question, Response
from .serializers import FormSerializer, QuestionSerializer, ResponseSerializer
import pprint


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


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save()
