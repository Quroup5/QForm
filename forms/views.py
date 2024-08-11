from rest_framework import viewsets, permissions
from .models import Form, Question
from .serializers import FormSerializer, QuestionSerializer


class IsFormOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsQuestionOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.form.user == request.user

    def has_permission(self, request, view):
        if view.action in ['create', 'list']:
            form_pk = view.kwargs.get('form_pk')
            if form_pk:
                try:
                    form = Form.objects.get(pk=form_pk)
                except Form.DoesNotExist:
                    return False
                return form.user == request.user

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
        form_pk = self.kwargs['form_pk']
        return Question.objects.filter(form_id=form_pk)
