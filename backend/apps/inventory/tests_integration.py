from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from apps.products.models import Product
from apps.inventory.models import StockMovement


class InventoryIntegrationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='inventoryuser', password='pass123')
        self.product = Product.objects.create(name='Test Product', price='10.00', stock=50)
        
    def authenticate(self):
        resp = self.client.post('/api/auth/login/', {'username': 'inventoryuser', 'password': 'pass123'}, format='json')
        token = resp.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    def test_list_stock_movements_requires_auth(self):
        url = '/api/inventory/movements/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_stock_movement_in(self):
        self.authenticate()
        url = '/api/inventory/movements/'
        data = {'product': self.product.id, 'movement_type': 'IN', 'quantity': 10, 'reason': 'Restock'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(StockMovement.objects.filter(product=self.product, movement_type='IN').exists())
        # Check stock updated
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 60)
    
    def test_create_stock_movement_out(self):
        self.authenticate()
        url = '/api/inventory/movements/'
        data = {'product': self.product.id, 'movement_type': 'OUT', 'quantity': 5, 'reason': 'Sale'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check stock updated
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 45)
    
    def test_create_stock_movement_adjustment(self):
        self.authenticate()
        url = '/api/inventory/movements/'
        data = {'product': self.product.id, 'movement_type': 'ADJUSTMENT', 'quantity': 100}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check stock adjusted to exact value
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 100)
    
    def test_list_stock_movements(self):
        self.authenticate()
        # Create a movement
        StockMovement.objects.create(product=self.product, movement_type='IN', quantity=20, user=self.user)
        url = '/api/inventory/movements/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
