from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from apps.orders.models import Order, OrderItem
from apps.products.models import Product


class OrderIntegrationTests(APITestCase):
    def setUp(self):
        # Crear usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
        # Crear productos de prueba
        self.product1 = Product.objects.create(
            name='Alimento para perros',
            price=50.00,
            stock=100
        )
        self.product2 = Product.objects.create(
            name='Collar',
            price=25.00,
            stock=50
        )
    
    def test_list_orders_requires_auth(self):
        """Listar pedidos requiere autenticación"""
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_order(self):
        """Crear un pedido con múltiples items"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'notes': 'Pedido de prueba',
            'items_data': [
                {'product_id': self.product1.id, 'quantity': 2},
                {'product_id': self.product2.id, 'quantity': 1}
            ]
        }
        
        response = self.client.post('/api/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total'], '125.00')  # (50*2) + (25*1)
        self.assertEqual(len(response.data['items']), 2)
        
        # Verificar que se redujo el stock
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.stock, 98)  # 100 - 2
        
        self.product2.refresh_from_db()
        self.assertEqual(self.product2.stock, 49)  # 50 - 1
    
    def test_create_order_insufficient_stock(self):
        """No permite crear pedido sin stock suficiente"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'notes': 'Pedido sin stock',
            'items_data': [
                {'product_id': self.product1.id, 'quantity': 200}  # Solo hay 100
            ]
        }
        
        response = self.client.post('/api/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Stock insuficiente', str(response.data))
    
    def test_list_orders(self):
        """Listar pedidos del usuario autenticado"""
        self.client.force_authenticate(user=self.user)
        
        # Crear pedido
        order = Order.objects.create(user=self.user, total=100.00)
        OrderItem.objects.create(
            order=order,
            product=self.product1,
            quantity=2,
            unit_price=50.00
        )
        
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], order.id)
    
    def test_order_detail(self):
        """Ver detalle de un pedido"""
        self.client.force_authenticate(user=self.user)
        
        order = Order.objects.create(user=self.user, total=50.00)
        OrderItem.objects.create(
            order=order,
            product=self.product1,
            quantity=1,
            unit_price=50.00
        )
        
        response = self.client.get(f'/api/orders/{order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], order.id)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product_name'], 'Alimento para perros')
    
    def test_filter_orders_by_status(self):
        """Filtrar pedidos por status"""
        self.client.force_authenticate(user=self.user)
        
        # Crear pedidos con diferentes status
        Order.objects.create(user=self.user, status='PENDING', total=100.00)
        Order.objects.create(user=self.user, status='COMPLETED', total=200.00)
        
        # Filtrar por PENDING
        response = self.client.get('/api/orders/?status=PENDING')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'PENDING')
        
        # Filtrar por COMPLETED
        response = self.client.get('/api/orders/?status=COMPLETED')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'COMPLETED')


class OrderDeliveryTests(APITestCase):
    """Tests para el sistema de delivery y tracking"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.staff = User.objects.create_user(username='staff', password='testpass123', is_staff=True)
        
        self.product = Product.objects.create(name='Test Product', price=100.00, stock=50)
        
        # Crear pedido base
        self.order = Order.objects.create(
            user=self.user,
            total=100.00,
            shipping_address='123 Test St, Test City'
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            unit_price=100.00
        )
    
    def test_order_has_delivery_fields(self):
        """Verificar que el pedido tiene campos de delivery"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/orders/{self.order.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('shipping_status', response.data)
        self.assertIn('tracking_number', response.data)
        self.assertIn('shipping_address', response.data)
        self.assertIn('estimated_delivery_date', response.data)
        self.assertEqual(response.data['shipping_status'], 'PENDING')
    
    def test_staff_can_update_shipping_status(self):
        """Staff puede actualizar estado de envío"""
        self.client.force_authenticate(user=self.staff)
        
        from datetime import date, timedelta
        
        data = {
            'shipping_status': 'SHIPPED',
            'tracking_number': 'TRACK123456',
            'estimated_delivery_date': str(date.today() + timedelta(days=3))
        }
        
        response = self.client.patch(f'/api/orders/{self.order.id}/shipping/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar actualización
        self.order.refresh_from_db()
        self.assertEqual(self.order.shipping_status, 'SHIPPED')
        self.assertEqual(self.order.tracking_number, 'TRACK123456')
        self.assertIsNotNone(self.order.shipped_date)
    
    def test_user_cannot_update_shipping_status(self):
        """Usuario normal no puede actualizar estado de envío"""
        self.client.force_authenticate(user=self.user)
        
        data = {'shipping_status': 'SHIPPED'}
        response = self.client.patch(f'/api/orders/{self.order.id}/shipping/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_track_order_by_tracking_number(self):
        """Consultar pedido por número de seguimiento sin autenticación"""
        self.order.tracking_number = 'TRACK999'
        self.order.shipping_status = 'IN_TRANSIT'
        self.order.save()
        
        # Sin autenticación
        response = self.client.get('/api/orders/tracking/TRACK999/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tracking_number'], 'TRACK999')
        self.assertEqual(response.data['shipping_status'], 'IN_TRANSIT')
    
    def test_track_order_invalid_tracking_number(self):
        """Tracking number inválido retorna 404"""
        response = self.client.get('/api/orders/tracking/INVALID123/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_my_orders_endpoint(self):
        """Usuario puede ver sus propios pedidos con info de envío"""
        # Crear otro pedido
        Order.objects.create(
            user=self.user,
            total=50.00,
            tracking_number='TRACK555',
            shipping_status='DELIVERED'
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/orders/my-orders/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verificar que tiene campos de delivery
        self.assertIn('shipping_status', response.data[0])
        self.assertIn('tracking_number', response.data[0])
    
    def test_filter_orders_by_shipping_status(self):
        """Filtrar pedidos por shipping_status"""
        # Crear pedidos con diferentes shipping_status
        Order.objects.create(
            user=self.user,
            total=50.00,
            shipping_status='DELIVERED'
        )
        Order.objects.create(
            user=self.user,
            total=75.00,
            shipping_status='IN_TRANSIT'
        )
        
        self.client.force_authenticate(user=self.user)
        
        # Filtrar por DELIVERED
        response = self.client.get('/api/orders/my-orders/?shipping_status=DELIVERED')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['shipping_status'], 'DELIVERED')
    
    def test_order_is_trackable_property(self):
        """Verificar propiedad is_trackable"""
        # Pedido sin tracking number
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/orders/{self.order.id}/')
        self.assertFalse(response.data['is_trackable'])
        
        # Agregar tracking number
        self.order.tracking_number = 'TRACK123'
        self.order.save()
        
        response = self.client.get(f'/api/orders/{self.order.id}/')
        self.assertTrue(response.data['is_trackable'])
    
    def test_order_can_be_delivered_property(self):
        """Verificar propiedad can_be_delivered"""
        self.client.force_authenticate(user=self.user)
        
        # Estado PENDING - no puede ser entregado
        response = self.client.get(f'/api/orders/{self.order.id}/')
        self.assertFalse(response.data['can_be_delivered'])
        
        # Estado SHIPPED - puede ser entregado
        self.order.shipping_status = 'SHIPPED'
        self.order.save()
        
        response = self.client.get(f'/api/orders/{self.order.id}/')
        self.assertTrue(response.data['can_be_delivered'])
    
    def test_delivered_date_auto_assigned(self):
        """Fecha de entrega se asigna automáticamente al marcar como DELIVERED"""
        self.client.force_authenticate(user=self.staff)
        
        data = {'shipping_status': 'DELIVERED'}
        response = self.client.patch(f'/api/orders/{self.order.id}/shipping/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertIsNotNone(self.order.delivered_date)
    
    def test_validation_shipped_requires_tracking(self):
        """Validar que SHIPPED requiere tracking_number"""
        self.client.force_authenticate(user=self.staff)
        
        data = {'shipping_status': 'SHIPPED'}  # Sin tracking_number
        response = self.client.patch(f'/api/orders/{self.order.id}/shipping/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('tracking_number', response.data)
    
    def test_shipping_status_display(self):
        """Verificar que shipping_status_display muestra texto legible"""
        self.order.shipping_status = 'IN_TRANSIT'
        self.order.save()
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/orders/{self.order.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('shipping_status_display', response.data)
        self.assertEqual(response.data['shipping_status_display'], 'En tránsito')
