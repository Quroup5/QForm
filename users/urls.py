from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from .views import UserViewSet, UserRegister

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegister.as_view(), name='register'),
    path('token-login/', views.obtain_auth_token)
]
