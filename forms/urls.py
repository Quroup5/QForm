from rest_framework.routers import DefaultRouter
from .views import FormViewSet, QuestionViewSet, ResponseViewSet

router = DefaultRouter()
router.register(r'forms', FormViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'responses', ResponseViewSet)

urlpatterns = [] + router.urls
