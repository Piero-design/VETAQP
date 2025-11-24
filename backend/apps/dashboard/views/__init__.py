from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Sum, Count, Q, Avg
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, date
from apps.orders.models import Order, OrderItem
from apps.products.models import Product
from apps.pets.models import Pet
from apps.appointments.models import Appointment
from apps.payments.models import Payment


class DashboardStatsView(APIView):
    """
    Vista principal del dashboard con estadísticas generales.
    Solo accesible para staff.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        # Calcular estadísticas generales
        total_orders = Order.objects.count()
        total_revenue = Order.objects.filter(status='COMPLETED').aggregate(
            total=Sum('total')
        )['total'] or 0
        
        active_users = User.objects.filter(is_active=True).count()
        total_pets = Pet.objects.count()
        total_products = Product.objects.count()
        low_stock_products = Product.objects.filter(stock__lte=10).count()
        
        # Estadísticas de pedidos por estado
        orders_by_status = Order.objects.values('status').annotate(
            count=Count('id')
        )
        
        # Estadísticas de envíos
        orders_by_shipping_status = Order.objects.values('shipping_status').annotate(
            count=Count('id')
        )
        
        # Citas
        total_appointments = Appointment.objects.count()
        pending_appointments = Appointment.objects.filter(status__in=['SCHEDULED', 'CONFIRMED']).count()
        
        # Estadísticas del mes actual
        current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        current_month_orders = Order.objects.filter(
            created_at__gte=current_month_start
        ).count()
        current_month_revenue = Order.objects.filter(
            created_at__gte=current_month_start,
            status='COMPLETED'
        ).aggregate(total=Sum('total'))['total'] or 0
        
        # Pagos
        total_payments = Payment.objects.count()
        successful_payments = Payment.objects.filter(status='COMPLETED').count()
        total_payments_amount = Payment.objects.filter(
            status='COMPLETED'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        return Response({
            'overview': {
                'total_orders': total_orders,
                'total_revenue': float(total_revenue),
                'active_users': active_users,
                'total_pets': total_pets,
                'total_products': total_products,
                'low_stock_products': low_stock_products,
                'total_appointments': total_appointments,
                'pending_appointments': pending_appointments,
            },
            'current_month': {
                'orders': current_month_orders,
                'revenue': float(current_month_revenue),
            },
            'orders_by_status': list(orders_by_status),
            'orders_by_shipping_status': list(orders_by_shipping_status),
            'payments': {
                'total': total_payments,
                'successful': successful_payments,
                'total_amount': float(total_payments_amount),
            }
        })


class SalesOverTimeView(APIView):
    """
    Ventas a lo largo del tiempo con agrupación configurable.
    Parámetros:
    - period: daily, weekly, monthly (default: daily)
    - start_date: fecha inicio (default: hace 30 días)
    - end_date: fecha fin (default: hoy)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        period = request.query_params.get('period', 'daily')
        
        # Fechas por defecto
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        
        # Parsear fechas si se proporcionan
        if request.query_params.get('start_date'):
            from dateutil import parser
            start_date = parser.parse(request.query_params.get('start_date'))
        
        if request.query_params.get('end_date'):
            from dateutil import parser
            end_date = parser.parse(request.query_params.get('end_date'))
        
        # Determinar función de truncado según período
        trunc_functions = {
            'daily': TruncDate,
            'weekly': TruncWeek,
            'monthly': TruncMonth,
        }
        
        trunc_func = trunc_functions.get(period, TruncDate)
        
        # Consultar ventas agrupadas
        sales = Order.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date,
            status='COMPLETED'
        ).annotate(
            period=trunc_func('created_at')
        ).values('period').annotate(
            total_orders=Count('id'),
            total_revenue=Sum('total')
        ).order_by('period')
        
        # Formatear respuesta
        result = [
            {
                'date': item['period'].isoformat() if item['period'] else None,
                'orders': item['total_orders'],
                'revenue': float(item['total_revenue'] or 0)
            }
            for item in sales
        ]
        
        return Response({
            'period': period,
            'start_date': start_date.date().isoformat(),
            'end_date': end_date.date().isoformat(),
            'data': result
        })


class PopularProductsView(APIView):
    """
    Productos más vendidos.
    Parámetros:
    - limit: cantidad de productos (default: 10)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        limit = int(request.query_params.get('limit', 10))
        
        # Calcular productos más vendidos
        from django.db.models import F
        popular_products = OrderItem.objects.values(
            'product__id',
            'product__name',
            'product__price'
        ).annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(F('unit_price') * F('quantity')),
            times_ordered=Count('order', distinct=True)
        ).order_by('-total_quantity')[:limit]
        
        result = [
            {
                'product_id': item['product__id'],
                'product_name': item['product__name'],
                'price': float(item['product__price']),
                'quantity_sold': item['total_quantity'],
                'revenue': float(item['total_revenue']),
                'times_ordered': item['times_ordered']
            }
            for item in popular_products
        ]
        
        return Response({
            'limit': limit,
            'products': result
        })


class AppointmentsStatsView(APIView):
    """
    Estadísticas de citas.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        # Estadísticas generales
        total = Appointment.objects.count()
        by_status = Appointment.objects.values('status').annotate(
            count=Count('id')
        )
        
        # Citas próximas (próximos 7 días)
        today = timezone.now().date()
        upcoming = Appointment.objects.filter(
            appointment_date__gte=today,
            appointment_date__lte=today + timedelta(days=7),
            status__in=['SCHEDULED', 'CONFIRMED']
        ).count()
        
        # Citas por mes (últimos 6 meses)
        six_months_ago = timezone.now() - timedelta(days=180)
        appointments_by_month = Appointment.objects.filter(
            appointment_date__gte=six_months_ago.date()
        ).annotate(
            month=TruncMonth('appointment_date')
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')
        
        monthly_data = [
            {
                'month': item['month'].strftime('%Y-%m'),
                'count': item['count']
            }
            for item in appointments_by_month
        ]
        
        return Response({
            'total': total,
            'by_status': list(by_status),
            'upcoming_7_days': upcoming,
            'monthly_trend': monthly_data
        })


class RecentActivityView(APIView):
    """
    Actividad reciente en el sistema.
    Parámetros:
    - limit: cantidad de items (default: 20)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        limit = int(request.query_params.get('limit', 20))
        
        # Órdenes recientes
        recent_orders = Order.objects.select_related('user').order_by('-created_at')[:limit]
        orders_data = [
            {
                'type': 'order',
                'id': order.id,
                'user': order.user.username,
                'status': order.status,
                'amount': float(order.total),
                'timestamp': order.created_at.isoformat()
            }
            for order in recent_orders
        ]
        
        # Citas recientes
        recent_appointments = Appointment.objects.select_related('user', 'pet').order_by('-created_at')[:limit]
        appointments_data = [
            {
                'type': 'appointment',
                'id': apt.id,
                'user': apt.user.username,
                'pet': apt.pet.name,
                'date': apt.appointment_date.isoformat(),
                'status': apt.status,
                'timestamp': apt.created_at.isoformat()
            }
            for apt in recent_appointments
        ]
        
        # Combinar y ordenar por timestamp
        all_activities = orders_data + appointments_data
        all_activities.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return Response({
            'limit': limit,
            'activities': all_activities[:limit]
        })


class LowStockProductsView(APIView):
    """
    Productos con stock bajo.
    Parámetros:
    - threshold: umbral de stock (default: 10)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        threshold = int(request.query_params.get('threshold', 10))
        
        low_stock = Product.objects.filter(
            stock__lte=threshold
        ).order_by('stock')
        
        result = [
            {
                'id': product.id,
                'name': product.name,
                'stock': product.stock,
                'price': float(product.price)
            }
            for product in low_stock
        ]
        
        return Response({
            'threshold': threshold,
            'count': len(result),
            'products': result
        })
