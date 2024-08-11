from rest_framework.routers import DefaultRouter
from .views import FormViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'forms', FormViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [] + router.urls
