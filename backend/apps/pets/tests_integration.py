from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from apps.pets.models import Pet


class PetsIntegrationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='petowner', password='pw')

    def authenticate_with_jwt(self):
        # obtain JWT token and set Authorization header for subsequent requests
        resp = self.client.post('/api/auth/login/', {'username': 'petowner', 'password': 'pw'}, format='json')
        token = resp.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_list_pets_empty(self):
        url = '/api/pets/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_create_pet_requires_auth(self):
        url = '/api/pets/'
        data = {'name': 'Fido', 'species': 'dog', 'age': 3, 'owner': self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_pet_authenticated(self):
        # authenticate using JWT (the API uses JWTAuthentication)
        self.authenticate_with_jwt()
        url = '/api/pets/'
        data = {'name': 'Fido', 'species': 'dog', 'age': 3, 'owner': self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Pet.objects.filter(name='Fido').exists())
