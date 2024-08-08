from rest_framework import viewsets, permissions
from .models import Form, Question
from .serializers import FormSerializer, QuestionSerializer


class IsOwner(permissions.BasePermission):
    """
    This class can be used to grant permission only to
    the owner of the model object in that model's `ModelViewSet`
    in the `permission_classes` list.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsQuestionOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.form.user == request.user


class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated, IsQuestionOwner]

    def perform_create(self, serializer):
        if self.request.data.get('type') == Question.TEXT:
            pass
        elif self.request.data.get('type') == Question.SELECT:
            pass
        elif self.request.data.get('type') == Question.CHECKBOX:
            pass

        serializer.save(data=self.request.data)
