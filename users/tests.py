from django.contrib.auth import get_user_model

from django.test import TestCase, Client
from django.urls import reverse, resolve
from rest_framework import status

from users.views import UserRegisterView, UserProfileUpdateView, OtpVerificationView, OtpRequestView


class TestUserAppURLs(TestCase):

    def test_register_url(self):
        url = reverse("register")
        self.assertEqual(resolve(url).func.view_class, UserRegisterView)

    def test_profile_update_url(self):
        url = reverse("update_profile")
        self.assertEqual(resolve(url).func.view_class, UserProfileUpdateView)

    def test_profile_otp_verify_url(self):
        url = reverse("otp_verify")
        self.assertEqual(resolve(url).func.view_class, OtpVerificationView)

    def test_profile_otp_request_url(self):
        url = reverse("otp_request")
        self.assertEqual(resolve(url).func.view_class, OtpRequestView)


class TestUserAppViews(TestCase):
    def setUP(self):
        self.client = Client()

    def test_register_view_with_no_data_passed(self):
        response = self.client.post(reverse("register"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_view_creating_one_user(self):
        self.username = "test_user"
        self.password = "123456"
        self.email = "test@test.com"

        data = {"username": self.username,
                "password": self.password,
                "email": self.email}

        response = self.client.post(reverse("register"), data=data)
        user = get_user_model().objects.first()
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.email, self.email)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_view_serializer_email_error(self):
        self.username = "test_user"
        self.password = "123456"
        self.email = "test_test.com"

        data = {"username": self.username,
                "password": self.password,
                "email": self.email}

        response = self.client.post(reverse("register"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUserAuthenticationViews(TestCase):

    def test_user_login(self):
        self.username = "test_user"
        self.password = "123456"
        self.email = "test@test.com"

        data = {"username": self.username,
                "password": self.password,
                "email": self.email}

        resp = self.client.post(reverse("register"), data=data)
        data = {"username": "test_user",
                "password": "123456"}

        response = self.client.post(reverse("JWT_token_obtain_pair"), data=data)

        response_data = response.json()

        access_token = response_data.get('access')
        refresh_token = response_data.get('refresh')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token)
        self.assertIsNotNone(refresh_token)

    def test_jwt_access_token_accessing_update_profile(self):
        self.username = "test_user"
        self.password = "123456"
        self.email = "test@test.com"

        data = {"username": self.username,
                "password": self.password,
                "email": self.email}

        response0 = self.client.post(reverse("register"), data=data)
        data = {"username": "test_user",
                "password": "123456"}

        response = self.client.post(reverse("JWT_token_obtain_pair"), data=data)

        response_data = response.json()

        access_token = response_data.get('access')
        refresh_token = response_data.get('refresh')
        data = {"firs_name": "updated_user",
                }
        auth_headers = {
            'Authorization': f'Bearer {access_token}',

        }

        response2 = self.client.put(reverse("update_profile"), data=data, )

        # TODO complete the test
