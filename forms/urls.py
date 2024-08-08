from rest_framework.routers import DefaultRouter
from .views import FormViewSet

router = DefaultRouter()
router.register(r'forms', FormViewSet)

urlpatterns = [] + router.urls
