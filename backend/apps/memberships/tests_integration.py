from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.memberships.models import Membership
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

User = get_user_model()


class MembershipIntegrationTests(APITestCase):
    def setUp(self):
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_list_memberships_requires_auth(self):
        """Test que listar membresías requiere autenticación"""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/memberships/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_membership(self):
        """Test crear una membresía"""
        data = {
            'plan_name': 'PREMIUM',
            'price': '99.90',
            'auto_renew': True,
            'duration_days': 30,
            'notes': 'Membresía premium con descuentos'
        }
        response = self.client.post('/api/memberships/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Membership.objects.count(), 1)
        
        membership = Membership.objects.first()
        self.assertEqual(membership.user, self.user)
        self.assertEqual(membership.plan_name, 'PREMIUM')
        self.assertEqual(membership.price, Decimal('99.90'))
        self.assertEqual(membership.status, 'ACTIVE')
        self.assertTrue(membership.auto_renew)
        self.assertEqual(membership.days_remaining, 30)
    
    def test_list_memberships(self):
        """Test listar membresías del usuario autenticado"""
        # Crear membresías de prueba
        Membership.objects.create(
            user=self.user,
            plan_name='BASIC',
            price=Decimal('49.90'),
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=30),
            status='ACTIVE'
        )
        Membership.objects.create(
            user=self.user,
            plan_name='VIP',
            price=Decimal('149.90'),
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=60),
            status='ACTIVE'
        )
        
        response = self.client.get('/api/memberships/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_membership_detail(self):
        """Test obtener detalle de una membresía"""
        membership = Membership.objects.create(
            user=self.user,
            plan_name='PREMIUM',
            price=Decimal('99.90'),
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=45),
            status='ACTIVE',
            auto_renew=True,
            notes='Membresía con beneficios premium'
        )
        
        response = self.client.get(f'/api/memberships/{membership.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['plan_name'], 'PREMIUM')
        self.assertEqual(response.data['status'], 'ACTIVE')
        self.assertEqual(response.data['user_username'], 'testuser')
        self.assertTrue(response.data['auto_renew'])
        self.assertEqual(response.data['days_remaining'], 45)
    
    def test_filter_memberships_by_status(self):
        """Test filtrar membresías por estado"""
        # Membresía activa
        Membership.objects.create(
            user=self.user,
            plan_name='BASIC',
            price=Decimal('49.90'),
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=30),
            status='ACTIVE'
        )
        # Membresía expirada
        Membership.objects.create(
            user=self.user,
            plan_name='PREMIUM',
            price=Decimal('99.90'),
            start_date=timezone.now().date() - timedelta(days=60),
            end_date=timezone.now().date() - timedelta(days=1),
            status='EXPIRED'
        )
        # Membresía cancelada
        Membership.objects.create(
            user=self.user,
            plan_name='VIP',
            price=Decimal('149.90'),
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=90),
            status='CANCELLED'
        )
        
        # Filtrar por ACTIVE
        response = self.client.get('/api/memberships/?status=ACTIVE')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'ACTIVE')
        
        # Filtrar por EXPIRED
        response = self.client.get('/api/memberships/?status=EXPIRED')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'EXPIRED')
