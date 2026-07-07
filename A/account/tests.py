from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

class RegisterTest(APITestCase):
    def test_user_can_register(self):
        url = reverse('account:user_register_api')
        data = {
            'username':'test',
            'email':'test@email.com',
            'password':'1234',
            'password2':'1234',
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username=data['username']).exists())

    def test_duplicate_username(self):
        User.objects.create_user(username='test', email='', password='1234')
        url = reverse('account:user_register_api')
        data = {
            'username':'test',
            'email':'test@email.com',
            'password':'1234',
            'password2':'1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(username=data['username']).count(), 1)

    def test_password_is_required(self):
        url = reverse('account:user_register_api')
        data = {
            'username':'test',
            'email':'test@email.com',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)