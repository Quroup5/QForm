from rest_framework import viewsets, permissions
from .models import Form
from .serializers import FormSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    This class can be used to grant permission only to
    the owner of the model object in that model's `ModelViewSet`
    in the `permission_classes` list.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
