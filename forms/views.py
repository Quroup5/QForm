from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import permissions, status, viewsets

from rest_framework.response import Response

from forms.models import Form
from forms.serializers import FormViewSetSerializer, FormUpdateViewSetSerializer, FormCreateViewSetSerializer


class FormViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "update":
            return FormUpdateViewSetSerializer
        if self.action == "create":
            return FormCreateViewSetSerializer
        return FormViewSetSerializer

    def get_queryset(self):
        return get_list_or_404(Form, user=self.request.user)

    def get_object(self):
        return get_object_or_404(Form, user=self.request.user, pk=self.kwargs.get('pk'))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        form = Form(title=serializer.validated_data.get('title'),
                    is_private=False,
                    user=request.user)

        if serializer.validated_data.get('password') is not None:
            form.is_private = True
            form.set_password(serializer.validated_data.get('password'))

        form.save()
        return Response(data={"title": serializer.validated_data.get('title')},
                        status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        form = get_object_or_404(Form, pk=self.get_object().pk, user=self.request.user)

        if serializer.validated_data.get('password') is not None:
            form.is_private = True
            form.set_password(serializer.data.get('password'))
        else:
            form.is_private = False
            form.password = None

        if serializer.validated_data.get('title') is not None:
            form.title = serializer.validated_data.get('title')

        if serializer.validated_data.get('password') is None and \
                serializer.validated_data.get('title') is None:
            return Response(data={"error": "Cannot left all fields blank!"}, status=status.HTTP_400_BAD_REQUEST)

        form.save()

        return Response(data={"title": form.title}, status=status.HTTP_205_RESET_CONTENT)
