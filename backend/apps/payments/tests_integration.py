from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.payments.models import Payment
from decimal import Decimal

User = get_user_model()


class PaymentIntegrationTests(APITestCase):
    def setUp(self):
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_list_payments_requires_auth(self):
        """Test que listar pagos requiere autenticación"""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/payments/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_payment(self):
        """Test crear un pago"""
        data = {
            'amount': '150.50',
            'payment_method': 'CARD',
            'transaction_id': 'TXN123456',
            'notes': 'Pago por servicios veterinarios'
        }
        response = self.client.post('/api/payments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 1)
        
        payment = Payment.objects.first()
        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.amount, Decimal('150.50'))
        self.assertEqual(payment.payment_method, 'CARD')
        self.assertEqual(payment.status, 'PENDING')
        self.assertEqual(payment.transaction_id, 'TXN123456')
    
    def test_list_payments(self):
        """Test listar pagos del usuario autenticado"""
        # Crear pagos de prueba
        Payment.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            payment_method='CASH',
            status='COMPLETED'
        )
        Payment.objects.create(
            user=self.user,
            amount=Decimal('200.00'),
            payment_method='YAPE',
            status='PENDING'
        )
        
        response = self.client.get('/api/payments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_payment_detail(self):
        """Test obtener detalle de un pago"""
        payment = Payment.objects.create(
            user=self.user,
            amount=Decimal('75.00'),
            payment_method='TRANSFER',
            status='COMPLETED',
            transaction_id='TXN789',
            notes='Pago de consulta'
        )
        
        response = self.client.get(f'/api/payments/{payment.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], '75.00')
        self.assertEqual(response.data['payment_method'], 'TRANSFER')
        self.assertEqual(response.data['status'], 'COMPLETED')
        self.assertEqual(response.data['user_username'], 'testuser')
    
    def test_filter_payments_by_status(self):
        """Test filtrar pagos por estado"""
        Payment.objects.create(
            user=self.user,
            amount=Decimal('50.00'),
            payment_method='CASH',
            status='COMPLETED'
        )
        Payment.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            payment_method='CARD',
            status='PENDING'
        )
        Payment.objects.create(
            user=self.user,
            amount=Decimal('150.00'),
            payment_method='YAPE',
            status='COMPLETED'
        )
        
        # Filtrar por COMPLETED
        response = self.client.get('/api/payments/?status=COMPLETED')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Filtrar por PENDING
        response = self.client.get('/api/payments/?status=PENDING')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'PENDING')
