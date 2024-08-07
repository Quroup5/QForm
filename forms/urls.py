from django.urls import path
from rest_framework.routers import DefaultRouter

from forms.views import FormViewSet

form_router = DefaultRouter()
form_router.register('', FormViewSet, basename="form_view_set")
urlpatterns = [] + form_router.urls
