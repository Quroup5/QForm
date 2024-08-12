from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from model_bakery import baker
from .models import Form, Category, Process, FormProcess


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


class CategoryViewSetTests(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        # Create test data
        self.category1 = baker.make(Category, title='Category 1', user=self.user)
        self.category2 = baker.make(Category, title='Category 2', user=self.user)

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


class ProcessViewSetTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user',
            password='test_password')
        self.client.force_authenticate(user=self.user)

        self.response = self.client.post(reverse("process-list"), data={"title": "test_title",
                                                                        "name": "test_name",
                                                                        "type": "linear"})

    def test_process_creation(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Process.objects.first().name, "test_name")
        self.assertEqual(Process.objects.first().type, "linear")
        self.assertEqual(Process.objects.first().title, "test_title")

    def test_process_delete(self):
        response = self.client.delete(reverse("process-detail"
                                              , args=[Process.objects.first().id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(Process.objects.first())

    def test_process_update(self):
        response = self.client.put(reverse("process-detail"
                                           , args=[Process.objects.first().id]),
                                   data={"title": "new_title",
                                         "name": "new_name",
                                         "type": "free"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Process.objects.first().name, "new_name")
        self.assertEqual(Process.objects.first().type, "free")
        self.assertEqual(Process.objects.first().title, "new_title")

    def test_process_detail(self):
        response = self.client.get(reverse("process-detail"
                                           , args=[Process.objects.first().id]))
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get("name"), "test_name")
        self.assertEqual(response_data.get("type"), "linear")
        self.assertEqual(response_data.get("title"), "test_title")


class FormProcessViewSetTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user',
            password='test_password')
        self.client.force_authenticate(user=self.user)
        self.form = Form(title="test_form", user=self.user)
        self.form.save()
        self.process = Process(**{"title": "test_title",
                                  "name": "test_process",
                                  "type": "linear"}, user=self.user)
        self.process.save()

        self.response = self.client.post(reverse("formprocess-list"), data={"form": 1,
                                                                            "process": 1,
                                                                            "order": 1})

    def test_formprocess_creation(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FormProcess.objects.first().process.name, "test_process")
        self.assertEqual(FormProcess.objects.first().form.title, "test_form")

    def test_formprocess_delete(self):
        response = self.client.delete(reverse("formprocess-detail"
                                              , args=[FormProcess.objects.first().id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(FormProcess.objects.first())

    def test_formprocess_update(self):
        response = self.client.put(reverse("formprocess-detail"
                                           , args=[Process.objects.first().id]),
                                   data={"form": 1,
                                         "process": 1,
                                         "order": 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FormProcess.objects.first().order, 2)

    def test_formprocess_detail(self):
        response = self.client.get(reverse("formprocess-detail"
                                           , args=[FormProcess.objects.first().id]))
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get("order"), 1)
