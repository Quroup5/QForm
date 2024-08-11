from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from model_bakery import baker
from .models import Form, Category, Process


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


class CategoryViewSetTests(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        # Create test data
        self.category1 = baker.make(Category, title='Category 1', user=self.user)
        self.category2 = baker.make(Category, title='Category 2', user=self.user)

        # Create related objects (optional, depending on your tests)
        self.form1 = baker.make(Form, title='Form 1', user=self.user)
        self.process1 = baker.make(Process, name='Process 1', title='Process 1', category=self.category1)

        # Add related objects to categories
        self.category1.forms.add(self.form1)
        self.category1.processes.add(self.process1)

    def test_create_category(self):
        response = self.client.post('/categories/', {
            'title': 'New Category',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'New Category')

    def test_list_categories(self):
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)  # Check if two categories exist

    def test_retrieve_category(self):
        response = self.client.get(f'/categories/{self.category1.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Category 1')

    def test_update_category(self):
        response = self.client.patch(f'/categories/{self.category1.id}/', {
            'title': 'Updated Category',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Updated Category')

    def test_delete_category(self):
        response = self.client.delete(f'/categories/{self.category1.id}/')
        self.assertEqual(response.status_code, 204)
        # Ensure the category is deleted
        response = self.client.get('/categories/')
        self.assertEqual(len([c for c in response.data if c['id'] == self.category1.id]), 0)
