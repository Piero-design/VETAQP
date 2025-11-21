from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class UsersIntegrationTests(APITestCase):
    def test_register_user(self):
        url = '/api/users/register/'
        data = {'username': 'tester', 'password': 'pass1234'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='tester').exists())

    def test_obtain_jwt_token(self):
        # create user then obtain token
        user = User.objects.create_user(username='tokenuser', password='strongpass')
        url = '/api/auth/login/'
        data = {'username': 'tokenuser', 'password': 'strongpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_me_requires_auth(self):
        url = '/api/users/me/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
