from rest_framework.routers import DefaultRouter
from .views import FormViewSet, QuestionViewSet

router = DefaultRouter()
router.register(r'forms', FormViewSet)
router.register(r'questions', QuestionViewSet)

urlpatterns = [] + router.urls
