from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from model_bakery import baker
from .models import Form


class FormViewSetTests(APITestCase):
    def setUp(self):
        self.user = baker.make(get_user_model())
        self.client.force_authenticate(user=self.user)
        self.url = reverse('form-list')

    def test_create_form(self):
        form_data = {
            'title': 'Test Form',
            'visitor_count': 0,
            'response_count': 0,
            'is_private': True,
            'password': 'supersecretpassword',
            'category': None
        }
        response = self.client.post(self.url, form_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        form = Form.objects.get(id=response.data['id'])

        self.assertNotEqual(form.password, form_data['password'])
        self.assertTrue(form.password.startswith('pbkdf2_'))

    def test_retrieve_form(self):
        form = baker.make(Form, user=self.user)

        response = self.client.get(reverse('form-detail', args=[form.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], form.title)

    def test_update_form(self):
        form = baker.make(Form, user=self.user, password=make_password('oldpassword'))

        updated_data = {
            'title': 'Updated Title',
            'password': 'newpassword',
        }

        response = self.client.put(reverse('form-detail', args=[form.id]), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        form.refresh_from_db()

        self.assertEqual(form.title, updated_data['title'])
        self.assertNotEqual(form.password, 'newpassword')
        self.assertTrue(form.password.startswith('pbkdf2_'))

    def test_delete_form(self):
        form = baker.make(Form, user=self.user)

        response = self.client.delete(reverse('form-detail', args=[form.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Form.objects.filter(id=form.id).exists())
