from rest_framework.routers import DefaultRouter
from .views import FormViewSet, ProcessViewSet, FormProcessViewSet, QuestionViewSet

router = DefaultRouter()
router.register(r'forms', FormViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'process', ProcessViewSet)
router.register(r'formprocess', FormProcessViewSet)
urlpatterns = [] + router.urls
