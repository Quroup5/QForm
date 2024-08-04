from random import randint

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CreateUserSerializer, OtpSerializerRequest, \
    OtpSerializerVerification, UserSerializer, UserProfileUpdateSerializer


class UserRegisterView(CreateAPIView):
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(data={"error": "Validation Error"}, status=status.HTTP_400_BAD_REQUEST)

        user_class = get_user_model()
        user_class.objects.create_user(username=serializer.data.get('username'),
                                       password=serializer.data.get('password'),
                                       email=serializer.data.get('email'))

        return Response(data={
            "msg": "User successfully created",
            "username": serializer.data.get('username'),
            "email": serializer.data.get('email'),
        },
            status=status.HTTP_201_CREATED)


class OtpRequestView(APIView):
    def post(self, request):
        serializer = OtpSerializerRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        target_user = get_object_or_404(get_user_model(),
                                        username=serializer.data.get('username'))

        if cache.get(target_user.id) is not None:
            return Response(data={"error": "Too many request you should wait for requesting new OTP. "},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)

        # This generates the otp and keeps it on cache memory
        generated_otp = str(randint(1000, 9999))
        print(f'Your one time password is : {generated_otp} \n',
              f'It will expires by one minute')
        cache.set(target_user.id, generated_otp, timeout=120)

        return Response(data={"msg": f'Your one time password is : {generated_otp}. '
                                     f'It will expires by one minute'},
                        status=status.HTTP_201_CREATED)


class OtpVerificationView(APIView):
    def post(self, request):
        serializer = OtpSerializerVerification(data=request.data)
        serializer.is_valid(raise_exception=True)

        target_user = get_object_or_404(get_user_model(),
                                        username=serializer.data.get('username'))

        sent_otp = cache.get(target_user.id)

        if sent_otp is None:
            return Response(data={"error": "Your OTP is expired. Request for new one!"},
                            status=status.HTTP_404_NOT_FOUND)

        if sent_otp != serializer.data.get("otp"):
            return Response(data={"error": "Wrong OTP!"},
                            status=status.HTTP_400_BAD_REQUEST)
        elif sent_otp == serializer.data.get("otp"):
            target_user.password = make_password(serializer.data.get('password'))
            target_user.save()

        return Response(data={"msg": f'Password of {target_user.username} changed!'},
                        status=status.HTTP_205_RESET_CONTENT)


class UserProfileUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):

        serializer = UserProfileUpdateSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.data.get("first_name"):
            self.request.user.first_name = serializer.data.get("first_name")

        if serializer.data.get("last_name"):
            self.request.user.last_name = serializer.data.get("last_name")

        if serializer.data.get("email"):
            self.request.user.email = serializer.data.get("email")

        self.request.user.save()

        return Response(data=serializer.data, status=status.HTTP_205_RESET_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
