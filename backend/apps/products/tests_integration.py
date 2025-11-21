from rest_framework import status
from rest_framework.test import APITestCase
from apps.products.models import Product


class ProductsIntegrationTests(APITestCase):
    def setUp(self):
        Product.objects.create(name='Shampoo', description='For fur', price='12.50', stock=10)

    def test_list_products(self):
        url = '/api/products/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_product_detail(self):
        prod = Product.objects.first()
        url = f'/api/products/{prod.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], prod.name)
