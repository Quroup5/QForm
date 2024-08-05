from django.shortcuts import get_object_or_404
from rest_framework import permissions, status

from rest_framework.response import Response
from rest_framework.views import APIView

from forms.models import Form, Category
from forms.serializers import CreateFormSerializer, UpdateFormSerializer


#
#
# class CreateQuestionView(CreateAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = CreateQuestionSerializer

class CreateFormView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = CreateFormSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        form = Form(title=serializer.data.get('title'),
                    is_private=False,
                    user=self.request.user)

        if serializer.data.get('password') is not None:
            form.is_private = True
            form.set_password(serializer.data.get('password'))

        form.save()

        return Response(data={
            "msg": "your form was created!",
            "form_id": form.id,
            "title": serializer.data.get("title")
        },
            status=status.HTTP_201_CREATED)


class UpdateFormView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        serializer = UpdateFormSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        form = get_object_or_404(Form,
                                 id=serializer.data.get("form_id"),
                                 user=self.request.user)

        if serializer.validated_data.get('password') is not None:
            form.is_private = True
            form.set_password(serializer.data.get('password'))

        if serializer.validated_data.get('category') is not None:
            category = Category(title=serializer.validated_data.get('category'))
            category.save()
            form.category = category


        if serializer.validated_data.get('title') is not None:
            form.title = serializer.validated_data.get('title')

        form.save()

        return Response(data={
            "msg": "your form was updated",
            "form_id": form.id,
            "title": form.title,
            "category": form.category.title
        },
            status=status.HTTP_201_CREATED)
