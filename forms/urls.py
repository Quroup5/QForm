from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FormViewSet, ProcessViewSet, FormProcessViewSet, QuestionViewSet, DisplayProcesView, DisplayFormView

router = DefaultRouter()
router.register(r'forms', FormViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'process', ProcessViewSet)
router.register(r'formprocess', FormProcessViewSet)
urlpatterns = [path("process/display/", DisplayProcesView.as_view(), name="display_process"),
               path("forms/display/", DisplayFormView.as_view(), name="display_form")
               ] + router.urls
