import json
import re
import requests
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from apps.products.models import Product


class SystemTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create initial data
        cls.superuser = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        Product.objects.create(name='Vaccine', description='Keeps pets healthy', price='20.00', stock=5)

    def test_admin_login_and_access(self):
        login_url = f'{self.live_server_url}/admin/login/'
        session = requests.Session()
        # get csrf token
        r = session.get(login_url)
        self.assertEqual(r.status_code, 200)
        # extract CSRF token from login page and perform login using admin credentials
        m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', r.text)
        csrf = m.group(1) if m else None
        login_data = {'username': 'admin', 'password': 'adminpass'}
        if csrf:
            login_data['csrfmiddlewaretoken'] = csrf
        # include Referer header so Django accepts the POST
        r2 = session.post(login_url, data=login_data, allow_redirects=True, headers={'Referer': login_url})
        # after login should be able to access admin index
        r3 = session.get(f'{self.live_server_url}/admin/')
        # admin site is localized; check for Spanish title or admin link text
        self.assertIn('Administración de Django', r3.text)

    def test_full_user_register_and_me(self):
        # register
        url = f'{self.live_server_url}/api/users/register/'
        # Register requires email and password length >=6 per serializer validation
        r = requests.post(url, json={'username': 'sysuser', 'password': 'strongpass', 'email': 'sysuser@example.com'})
        self.assertEqual(r.status_code, 201)
        # login to obtain JWT (try JSON, then form-encoded as fallback)
        token_url = f'{self.live_server_url}/api/auth/login/'
        r2 = requests.post(token_url, json={'username': 'sysuser', 'password': 'strongpass'})
        if r2.status_code == 401:
            r2 = requests.post(token_url, data={'username': 'sysuser', 'password': 'strongpass'})
        self.assertEqual(r2.status_code, 200, msg=f'Login failed: {r2.status_code} {r2.text}')
        access = r2.json().get('access')
        self.assertIsNotNone(access)
        # call /me
        r3 = requests.get(f'{self.live_server_url}/api/users/me/', headers={'Authorization': f'Bearer {access}'})
        self.assertEqual(r3.status_code, 200)

    def test_pet_crud_via_api(self):
        # create user and token
        user = User.objects.create_user('petuser', password='pw')
        r = requests.post(f'{self.live_server_url}/api/auth/login/', json={'username': 'petuser', 'password': 'pw'})
        token = r.json().get('access')
        headers = {'Authorization': f'Bearer {token}'}
        # create pet
        data = {'name': 'Buddy', 'species': 'dog', 'age': 2, 'owner': user.id}
        r2 = requests.post(f'{self.live_server_url}/api/pets/', json=data, headers=headers)
        self.assertEqual(r2.status_code, 201)
        pet_id = r2.json().get('id')
        # update pet
        r3 = requests.patch(f'{self.live_server_url}/api/pets/{pet_id}/', json={'age': 3}, headers=headers)
        self.assertIn(r3.status_code, (200, 202))
        # delete pet
        r4 = requests.delete(f'{self.live_server_url}/api/pets/{pet_id}/', headers=headers)
        self.assertIn(r4.status_code, (204, 200))

    def test_product_listing_public(self):
        r = requests.get(f'{self.live_server_url}/api/products/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertTrue(isinstance(data, list))

    def test_cors_allows_origin(self):
        # simulate request from frontend origin
        r = requests.get(f'{self.live_server_url}/api/products/', headers={'Origin': 'http://localhost:5173'})
        self.assertEqual(r.status_code, 200)
        # CORS should expose header
        self.assertIn('access-control-allow-origin', r.headers)
