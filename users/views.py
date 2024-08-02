from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, CreateUserSerializer
from .models import User


class UserRegister(APIView):
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)

        except ValidationError:
            return Response(data={"Validation Error"}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(username=serializer.data.get('username'),
                                 password=serializer.data.get('password'),
                                 email=serializer.data.get('email'))

        return Response(status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
