from django.urls import path
from graphene_django.views import GraphQLView
from rest_framework.routers import DefaultRouter

from .schema import schema
from .views import FormViewSet, ProcessViewSet, FormProcessViewSet, QuestionViewSet, DisplayProcesView, DisplayFormView, \
    CategoryViewSet

router = DefaultRouter()
router.register(r'forms', FormViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'process', ProcessViewSet)
router.register(r'formprocess', FormProcessViewSet)
router.register(r'categories', CategoryViewSet)
urlpatterns = [path("process/display/", DisplayProcesView.as_view(), name="display_process"),
               path("forms/display/", DisplayFormView.as_view(), name="display_form"),
               path("GQL/", GraphQLView.as_view(graphiql=True, schema=schema), name="GQL")
               ] + router.urls
