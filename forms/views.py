from rest_framework import viewsets, permissions
from .models import Form, Question
from .serializers import FormSerializer, QuestionSerializer


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
