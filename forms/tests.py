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


class QuestionViewSetTests(APITestCase):
    def setUp(self):
        self.user = baker.make('users.User')
        self.form = baker.make(Form, user=self.user)
        self.client.force_authenticate(user=self.user)
        self.url = reverse('question-list')

    def test_create_text_question(self):
        data = {
            'name': 'Question 1',
            'label': 'What is your name?',
            'required': True,
            'type': 'text',
            'metadata': {},  # Should be empty
            'form': self.form.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_select_question(self):
        data = {
            'name': 'Question 2',
            'label': 'Choose a fruit',
            'required': True,
            'type': 'select',
            'metadata': {
                'selectbox1': 'Apple',
                'selectbox2': 'Banana',
                'selectbox3': 'Cherry',
            },
            'form': self.form.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_metadata_for_text_question(self):
        data = {
            'name': 'Question 3',
            'label': 'Invalid Text Question',
            'required': True,
            'type': 'text',
            'metadata': {
                'key': 'This should not be here'
            },
            'form': self.form.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('metadata', response.data)

    def test_invalid_metadata_structure(self):
        data = {
            'name': 'Question 4',
            'label': 'Invalid Select Question',
            'required': True,
            'type': 'select',
            'metadata': ['Invalid structure'],  # Should be a dictionary
            'form': self.form.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('metadata', response.data)

    def test_valid_dynamic_select_metadata(self):
        data = {
            'name': 'Question 2',
            'label': 'Choose options',
            'required': True,
            'type': 'select',
            'metadata': {
                'selectbox1': 'Option 1',
                'selectbox2': 'Option 2',
                'selectbox3': 'Option 3',
            },
            'form': self.form.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_dynamic_metadata_key(self):
        data = {
            'name': 'Question 3',
            'label': 'Choose options',
            'required': True,
            'type': 'select',
            'metadata': {
                'wrongkey1': 'Option 1',  # Invalid key
                'selectbox2': 'Option 2'
            },
            'form': self.form.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('metadata', response.data)

    def test_invalid_dynamic_metadata_value(self):
        data = {
            'name': 'Question 4',
            'label': 'Choose options',
            'required': True,
            'type': 'checkbox',
            'metadata': {
                'checkbox1': 100,  # Invalid value, should be a string
                'checkbox2': 'Option 2'
            },
            'form': self.form.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('metadata', response.data)
