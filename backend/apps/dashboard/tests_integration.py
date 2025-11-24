from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, date
from apps.orders.models import Order, OrderItem
from apps.products.models import Product
from apps.pets.models import Pet
from apps.appointments.models import Appointment
from apps.payments.models import Payment


class DashboardStatsTests(APITestCase):
    """Tests para el dashboard de estadísticas"""
    
    def setUp(self):
        # Crear usuarios
        self.staff = User.objects.create_user(
            username='admin',
            password='admin123',
            is_staff=True
        )
        self.user = User.objects.create_user(
            username='user',
            password='user123'
        )
        
        # Crear datos de prueba
        self.product1 = Product.objects.create(
            name='Product 1',
            price=100.00,
            stock=50
        )
        self.product2 = Product.objects.create(
            name='Product 2',
            price=50.00,
            stock=5  # Low stock
        )
        
        # Crear órdenes
        self.order1 = Order.objects.create(
            user=self.user,
            status='COMPLETED',
            total=200.00
        )
        OrderItem.objects.create(
            order=self.order1,
            product=self.product1,
            quantity=2,
            unit_price=100.00
        )
        
        self.order2 = Order.objects.create(
            user=self.user,
            status='PENDING',
            total=50.00
        )
        
        # Crear mascota y cita
        self.pet = Pet.objects.create(
            name='Firulais',
            species='Perro',
            age=3,
            owner=self.user
        )
        
        self.appointment = Appointment.objects.create(
            user=self.user,
            pet=self.pet,
            appointment_date=date.today() + timedelta(days=2),
            appointment_time='10:00:00',
            reason='Chequeo',
            status='SCHEDULED'
        )
        
        # Crear pago
        Payment.objects.create(
            user=self.user,
            order=self.order1,
            amount=200.00,
            payment_method='CREDIT_CARD',
            status='COMPLETED'
        )
    
    def test_dashboard_stats_requires_staff(self):
        """Solo staff puede acceder al dashboard"""
        # Usuario normal
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/dashboard/stats/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Sin autenticación
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/dashboard/stats/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_dashboard_stats_success(self):
        """Staff puede obtener estadísticas del dashboard"""
        self.client.force_authenticate(user=self.staff)
        response = self.client.get('/api/dashboard/stats/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar estructura de respuesta
        self.assertIn('overview', response.data)
        self.assertIn('current_month', response.data)
        self.assertIn('orders_by_status', response.data)
        self.assertIn('payments', response.data)
        
        # Verificar valores
        overview = response.data['overview']
        self.assertEqual(overview['total_orders'], 2)
        self.assertEqual(overview['total_revenue'], 200.00)  # Solo COMPLETED
        self.assertEqual(overview['active_users'], 2)
        self.assertEqual(overview['total_pets'], 1)
        self.assertEqual(overview['total_products'], 2)
        self.assertEqual(overview['low_stock_products'], 1)
        self.assertEqual(overview['total_appointments'], 1)
        self.assertEqual(overview['pending_appointments'], 1)
    
    def test_sales_over_time_daily(self):
        """Consultar ventas por día"""
        self.client.force_authenticate(user=self.staff)
        
        response = self.client.get('/api/dashboard/sales-over-time/?period=daily')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['period'], 'daily')
        self.assertIn('data', response.data)
    
    def test_sales_over_time_with_date_range(self):
        """Consultar ventas con rango de fechas"""
        self.client.force_authenticate(user=self.staff)
        
        start = (timezone.now() - timedelta(days=7)).date().isoformat()
        end = timezone.now().date().isoformat()
        
        response = self.client.get(
            f'/api/dashboard/sales-over-time/?period=daily&start_date={start}&end_date={end}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['start_date'], start)
        self.assertEqual(response.data['end_date'], end)
    
    def test_popular_products(self):
        """Consultar productos más vendidos"""
        self.client.force_authenticate(user=self.staff)
        
        response = self.client.get('/api/dashboard/popular-products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn('products', response.data)
        self.assertEqual(len(response.data['products']), 1)  # Solo 1 producto vendido
        
        product = response.data['products'][0]
        self.assertEqual(product['product_name'], 'Product 1')
        self.assertEqual(product['quantity_sold'], 2)
    
    def test_popular_products_with_limit(self):
        """Limitar cantidad de productos retornados"""
        self.client.force_authenticate(user=self.staff)
        
        response = self.client.get('/api/dashboard/popular-products/?limit=5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['limit'], 5)
    
    def test_appointments_stats(self):
        """Consultar estadísticas de citas"""
        self.client.force_authenticate(user=self.staff)
        
        response = self.client.get('/api/dashboard/appointments-stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['total'], 1)
        self.assertEqual(response.data['upcoming_7_days'], 1)
        self.assertIn('by_status', response.data)
        self.assertIn('monthly_trend', response.data)
    
    def test_recent_activity(self):
        """Consultar actividad reciente"""
        self.client.force_authenticate(user=self.staff)
        
        response = self.client.get('/api/dashboard/recent-activity/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn('activities', response.data)
        activities = response.data['activities']
        
        # Debe haber órdenes y citas
        types = [activity['type'] for activity in activities]
        self.assertIn('order', types)
        self.assertIn('appointment', types)
    
    def test_recent_activity_with_limit(self):
        """Limitar actividad reciente"""
        self.client.force_authenticate(user=self.staff)
        
        response = self.client.get('/api/dashboard/recent-activity/?limit=5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['limit'], 5)
        self.assertLessEqual(len(response.data['activities']), 5)
    
    def test_low_stock_products(self):
        """Consultar productos con stock bajo"""
        self.client.force_authenticate(user=self.staff)
        
        response = self.client.get('/api/dashboard/low-stock/?threshold=10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['threshold'], 10)
        self.assertEqual(response.data['count'], 1)
        
        products = response.data['products']
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]['name'], 'Product 2')
        self.assertEqual(products[0]['stock'], 5)
    
    def test_low_stock_custom_threshold(self):
        """Usar umbral personalizado para stock bajo"""
        self.client.force_authenticate(user=self.staff)
        
        response = self.client.get('/api/dashboard/low-stock/?threshold=3')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)  # Ninguno bajo 3
        
        response = self.client.get('/api/dashboard/low-stock/?threshold=60')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)  # Ambos bajo 60
    
    def test_all_endpoints_require_staff(self):
        """Verificar que todos los endpoints requieren permisos de staff"""
        self.client.force_authenticate(user=self.user)
        
        endpoints = [
            '/api/dashboard/stats/',
            '/api/dashboard/sales-over-time/',
            '/api/dashboard/popular-products/',
            '/api/dashboard/appointments-stats/',
            '/api/dashboard/recent-activity/',
            '/api/dashboard/low-stock/',
        ]
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
                f"Endpoint {endpoint} should require staff permission"
            )
