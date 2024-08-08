from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.generics import CreateAPIView

# from forms.serializers import CreateQuestionSerializer
#
#
# class CreateQuestionView(CreateAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = CreateQuestionSerializer
