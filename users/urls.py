from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from .views import UserViewSet, UserRegister
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegister.as_view(), name='register'),
    path('token-login/', views.obtain_auth_token),
    path('token/verify/', TokenVerifyView.as_view(), name='JWT_token_verify'),
    path('token/obtain/', TokenObtainPairView.as_view(), name='JWT_token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='JWT_token_refresh'),
]
