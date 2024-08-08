from django.urls import path
from rest_framework import routers

from .views import UserViewSet, UserRegisterView, OtpVerificationView,OtpRequestView, UserProfileUpdateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
                  path('register/', UserRegisterView.as_view(), name='register'),
                  path('profile/update/', UserProfileUpdateView.as_view(), name='update_profile'),
                  path('token/verify/', TokenVerifyView.as_view(), name='JWT_token_verify'),
                  path('token/obtain/', TokenObtainPairView.as_view(), name='JWT_token_obtain_pair'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='JWT_token_refresh'),
                  path('otp/verify/', OtpVerificationView.as_view(), name='otp_verify'),
                  path('otp/request/', OtpRequestView.as_view(), name='otp_request'),

              ] + router.urls
