# 📊 Dashboard de Administración - Documentación Técnica

## 🎯 Objetivo

Proporcionar una vista consolidada de métricas y análisis de negocio para usuarios administradores (staff), permitiendo tomar decisiones basadas en datos sobre inventario, ventas, citas y actividad general del sistema.

---

## 🏗️ Arquitectura

### Backend: Django REST Framework

```
apps/dashboard/
├── __init__.py
├── apps.py                    # Configuración de la app
├── views/
│   └── __init__.py           # 6 vistas de analytics (APIView)
├── urls.py                    # Rutas del dashboard
└── tests_integration.py       # Suite de 12 tests
```

### Frontend: React + Tailwind CSS

```
frontend/src/pages/
└── Dashboard.jsx              # Componente principal (~400 líneas)
```

---

## 📡 API Endpoints

### 1. Estadísticas Generales
**Endpoint:** `GET /api/dashboard/stats/`  
**Permisos:** Staff only  
**Descripción:** Métricas principales del sistema

**Response:**
```json
{
  "overview": {
    "total_orders": 150,
    "total_revenue": 15000.00,
    "active_users": 85,
    "total_pets": 120,
    "total_products": 45,
    "low_stock_products": 3,
    "total_appointments": 200,
    "pending_appointments": 12
  },
  "current_month": {
    "orders": 25,
    "revenue": 2500.00
  },
  "orders_by_status": {
    "PENDING": 10,
    "PROCESSING": 8,
    "SHIPPED": 5,
    "DELIVERED": 20,
    "CANCELLED": 2
  },
  "orders_by_shipping_status": {
    "PENDING": 10,
    "PROCESSING": 8,
    "SHIPPED": 5,
    "DELIVERED": 20
  },
  "payments": {
    "total": 45,
    "successful": 42,
    "failed": 3,
    "total_amount": 15000.00
  }
}
```

**Casos de uso:**
- Dashboard principal con cards de métricas
- Monitoreo de KPIs en tiempo real
- Comparativa mes actual vs histórico

---

### 2. Ventas en el Tiempo
**Endpoint:** `GET /api/dashboard/sales-over-time/`  
**Permisos:** Staff only  
**Parámetros:**
- `period` (string): `daily`, `weekly`, `monthly` - Default: `daily`
- `start_date` (date): YYYY-MM-DD - Opcional
- `end_date` (date): YYYY-MM-DD - Opcional

**Response:**
```json
{
  "period": "daily",
  "start_date": "2025-01-01",
  "end_date": "2025-01-15",
  "data": [
    {
      "date": "2025-01-01",
      "orders": 5,
      "revenue": 500.00
    },
    {
      "date": "2025-01-02",
      "orders": 8,
      "revenue": 750.00
    }
  ]
}
```

**Implementación Backend:**
```python
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth

# Truncate según periodo
trunc_fn = {
    'daily': TruncDate,
    'weekly': TruncWeek,
    'monthly': TruncMonth
}[period]

# Agregación
orders = Order.objects.filter(
    created_at__range=[start_date, end_date]
).annotate(
    date=trunc_fn('created_at')
).values('date').annotate(
    orders=Count('id'),
    revenue=Sum('total_amount')
).order_by('date')
```

**Casos de uso:**
- Gráficos de tendencia de ventas
- Análisis de períodos de alta/baja demanda
- Comparativas entre diferentes períodos
- Forecasting de ventas

---

### 3. Productos Populares
**Endpoint:** `GET /api/dashboard/popular-products/`  
**Permisos:** Staff only  
**Parámetros:**
- `limit` (int): Cantidad de productos a retornar - Default: 10

**Response:**
```json
{
  "products": [
    {
      "product_id": 1,
      "product_name": "Alimento Premium Adulto 15kg",
      "quantity_sold": 150,
      "revenue": 4500.00,
      "times_ordered": 45
    },
    {
      "product_id": 2,
      "product_name": "Shampoo Medicado",
      "quantity_sold": 80,
      "revenue": 2000.00,
      "times_ordered": 32
    }
  ]
}
```

**Implementación Backend:**
```python
from django.db.models import F, Sum, Count

products = OrderItem.objects.values(
    'product_id',
    'product__name'
).annotate(
    quantity_sold=Sum('quantity'),
    revenue=Sum(F('unit_price') * F('quantity')),
    times_ordered=Count('order', distinct=True)
).order_by('-quantity_sold')[:limit]
```

**Nota técnica:** Se usa `F('unit_price') * F('quantity')` en lugar de `Sum('subtotal')` porque `subtotal` es una propiedad del modelo, no un campo de BD.

**Casos de uso:**
- Identificar productos más vendidos
- Planificación de stock
- Decisiones de marketing (promociones)
- Análisis de rentabilidad

---

### 4. Estadísticas de Citas
**Endpoint:** `GET /api/dashboard/appointments-stats/`  
**Permisos:** Staff only

**Response:**
```json
{
  "total_appointments": 200,
  "by_status": {
    "SCHEDULED": 50,
    "CONFIRMED": 30,
    "COMPLETED": 100,
    "CANCELLED": 20
  },
  "upcoming_7_days": 12,
  "monthly_trend": [
    {
      "month": "2024-08-01",
      "count": 35
    },
    {
      "month": "2024-09-01",
      "count": 42
    }
  ]
}
```

**Implementación Backend:**
```python
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth

# Próximas 7 días
upcoming = Appointment.objects.filter(
    appointment_date__range=[
        datetime.now().date(),
        datetime.now().date() + timedelta(days=7)
    ],
    status__in=['SCHEDULED', 'CONFIRMED']
).count()

# Tendencia mensual (últimos 6 meses)
six_months_ago = datetime.now() - timedelta(days=180)
monthly = Appointment.objects.filter(
    appointment_date__gte=six_months_ago
).annotate(
    month=TruncMonth('appointment_date')
).values('month').annotate(
    count=Count('id')
).order_by('month')
```

**Casos de uso:**
- Planificación de recursos veterinarios
- Identificación de días/horas pico
- Proyección de carga de trabajo
- Alertas de saturación de agenda

---

### 5. Actividad Reciente
**Endpoint:** `GET /api/dashboard/recent-activity/`  
**Permisos:** Staff only  
**Parámetros:**
- `limit` (int): Cantidad de actividades - Default: 20

**Response:**
```json
{
  "activities": [
    {
      "id": 123,
      "type": "order",
      "user": "juan.perez",
      "amount": 150.00,
      "status": "PROCESSING",
      "timestamp": "2025-01-15T10:30:00Z"
    },
    {
      "id": 456,
      "type": "appointment",
      "user": "maria.garcia",
      "pet": "Max",
      "status": "SCHEDULED",
      "timestamp": "2025-01-15T09:15:00Z"
    }
  ]
}
```

**Implementación Backend:**
```python
# Obtener pedidos recientes
orders = Order.objects.select_related('user').order_by('-created_at')[:limit]
order_activities = [{
    'id': o.id,
    'type': 'order',
    'user': o.user.username,
    'amount': float(o.total_amount),
    'status': o.status,
    'timestamp': o.created_at.isoformat()
} for o in orders]

# Obtener citas recientes
appointments = Appointment.objects.select_related(
    'user', 'pet'
).order_by('-created_at')[:limit]
appointment_activities = [{
    'id': a.id,
    'type': 'appointment',
    'user': a.user.username,
    'pet': a.pet.name,
    'status': a.status,
    'timestamp': a.created_at.isoformat()
} for a in appointments]

# Combinar y ordenar
all_activities = sorted(
    order_activities + appointment_activities,
    key=lambda x: x['timestamp'],
    reverse=True
)[:limit]
```

**Casos de uso:**
- Feed de actividad en tiempo real
- Monitoreo de transacciones
- Detección de anomalías
- Auditoría de operaciones

---

### 6. Productos con Stock Bajo
**Endpoint:** `GET /api/dashboard/low-stock/`  
**Permisos:** Staff only  
**Parámetros:**
- `threshold` (int): Nivel de stock para considerar "bajo" - Default: 10

**Response:**
```json
{
  "products": [
    {
      "id": 5,
      "name": "Shampoo Medicado",
      "stock": 3,
      "price": 25.00
    },
    {
      "id": 12,
      "name": "Collar Antipulgas",
      "stock": 7,
      "price": 15.00
    }
  ]
}
```

**Implementación Backend:**
```python
products = Product.objects.filter(
    stock__lt=threshold,
    stock__gt=0
).order_by('stock').values(
    'id', 'name', 'stock', 'price'
)
```

**Casos de uso:**
- Alertas de reabastecimiento
- Prevención de quiebres de stock
- Optimización de compras
- Gestión de inventario crítico

---

## 🎨 Frontend - Dashboard UI

### Componente Principal: `Dashboard.jsx`

**Características:**
- ✅ Verificación automática de permisos staff
- ✅ Carga paralela de 6 endpoints
- ✅ Manejo de estados: loading, error, success
- ✅ Responsive design (mobile-first)
- ✅ Cards informativos con iconos
- ✅ Selector de período para ventas
- ✅ Formateo de moneda (PEN)
- ✅ Formateo de fechas (es-ES)
- ✅ Color coding por estado

### Estructura Visual

```
┌─────────────────────────────────────────────────────────┐
│  📊 Dashboard de Administración                         │
│  Panel de control y estadísticas generales              │
└─────────────────────────────────────────────────────────┘

┌──────────────┬──────────────┬──────────────┬──────────────┐
│ 🛒 Pedidos   │ 💰 Ingresos  │ 👥 Usuarios  │ 📅 Citas     │
│ 150          │ S/ 15,000    │ 85           │ 12 pendientes│
│ Mes: 25      │ Mes: S/ 2.5K │ 120 mascotas │ Total: 200   │
└──────────────┴──────────────┴──────────────┴──────────────┘

┌──────────────┬──────────────┬──────────────┐
│ 📦 Productos │ 💳 Pagos     │ 📊 Tasa Éxito│
│ 45           │ 42 exitosos  │ 93%          │
│ 3 stock bajo │ Total: S/15K │ 45 pagos     │
└──────────────┴──────────────┴──────────────┘

┌─────────────────────────────────────────────────────────┐
│  Ventas a lo Largo del Tiempo     [Diario ▼]           │
│  ─────────────────────────────────────────────────      │
│  2025-01-10 ············ 5 pedidos ······ S/ 500.00    │
│  2025-01-11 ············ 8 pedidos ······ S/ 750.00    │
│  2025-01-12 ············ 3 pedidos ······ S/ 300.00    │
└─────────────────────────────────────────────────────────┘

┌────────────────────────────┬─────────────────────────────┐
│  Productos Más Vendidos    │  Productos con Stock Bajo   │
│  ──────────────────────    │  ─────────────────────────  │
│  #1 Alimento Premium       │  🔴 Shampoo Medicado        │
│      150 unidades          │      Stock: 3 unidades      │
│      S/ 4,500.00           │      S/ 25.00               │
│                            │                             │
│  #2 Collar Antipulgas      │  🔴 Collar Antipulgas       │
│      80 unidades           │      Stock: 7 unidades      │
│      S/ 2,000.00           │      S/ 15.00               │
└────────────────────────────┴─────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Actividad Reciente                                     │
│  ─────────────────────────────────────────────────      │
│  🛒 Pedido #123                          PROCESSING     │
│     juan.perez - S/ 150.00       15 Ene 10:30          │
│                                                          │
│  📅 Cita #456                            SCHEDULED      │
│     maria.garcia - Max           15 Ene 09:15          │
└─────────────────────────────────────────────────────────┘
```

### Estados de Carga

```jsx
// Loading
<div className="text-center py-12">
  <div className="text-2xl">Cargando dashboard...</div>
</div>

// Error
<div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
  {error}
</div>

// No autorizado
<div className="bg-red-100 ...">
  No tienes permisos para acceder al dashboard
</div>
```

### Componentes Reutilizables

#### StatCard
```jsx
<StatCard
  title="Total Pedidos"
  value={150}
  subtitle="Mes actual: 25"
  icon="🛒"
  color="blue"
/>
```

Props:
- `title` (string): Título de la métrica
- `value` (string|number): Valor principal
- `subtitle` (string): Texto secundario
- `icon` (emoji): Ícono visual
- `color` (string): Tailwind color (blue, green, purple, orange)

---

## 🧪 Tests

### Suite Completa: 12 Tests

```bash
cd backend
python manage.py test apps.dashboard.tests_integration -v 2
```

### Tests Implementados

#### 1. **test_dashboard_stats_requires_staff**
**Objetivo:** Verificar que solo usuarios staff pueden acceder  
**Casos:**
- Usuario anónimo → 401 Unauthorized
- Usuario regular → 403 Forbidden
- Usuario staff → 200 OK

```python
# Usuario regular intenta acceder
response = self.client.get(
    self.url,
    HTTP_AUTHORIZATION=f'Bearer {self.user_token}'
)
self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
```

#### 2. **test_dashboard_stats_success**
**Objetivo:** Validar estructura y valores de respuesta  
**Verificaciones:**
- Claves presentes: overview, current_month, orders_by_status, payments
- Valores correctos basados en datos de prueba
- Tipos de datos correctos (int, float)

```python
self.assertEqual(data['overview']['total_orders'], 2)
self.assertEqual(float(data['overview']['total_revenue']), 200.00)
self.assertEqual(data['overview']['active_users'], 2)
```

#### 3. **test_sales_over_time_daily**
**Objetivo:** Verificar agregación diaria  
**Setup:**
- Crear 2 órdenes en fechas diferentes
- Solicitar período `daily`
- Validar estructura de respuesta

```python
response = self.staff_client.get(f'{self.sales_url}?period=daily')
self.assertEqual(response.status_code, status.HTTP_200_OK)
self.assertIn('data', response.data)
self.assertIsInstance(response.data['data'], list)
```

#### 4. **test_sales_over_time_with_date_range**
**Objetivo:** Probar filtros de fecha  
**Casos:**
- start_date y end_date válidos
- Solo órdenes en rango deben retornarse
- Formato de fecha correcto

```python
params = {
    'period': 'daily',
    'start_date': '2025-11-17',
    'end_date': '2025-11-24'
}
response = self.staff_client.get(self.sales_url, params)
# Verificar que solo órdenes en rango se incluyen
```

#### 5. **test_popular_products**
**Objetivo:** Validar cálculo de popularidad  
**Setup:**
- Producto 1: 2 unidades vendidas
- Producto 2: 1 unidad vendida
**Verificaciones:**
- Producto 1 primero (mayor cantidad)
- quantity_sold correcto
- revenue calculado correctamente

```python
self.assertEqual(data['products'][0]['quantity_sold'], 2)
self.assertEqual(data['products'][0]['product_id'], self.product1.id)
```

#### 6. **test_popular_products_with_limit**
**Objetivo:** Validar parámetro limit  
**Setup:** Crear 3 productos
**Test:** `?limit=2` debe retornar solo 2 productos

```python
response = self.staff_client.get(f'{self.popular_url}?limit=2')
self.assertEqual(len(response.data['products']), 2)
```

#### 7. **test_appointments_stats**
**Objetivo:** Verificar estadísticas de citas  
**Verificaciones:**
- Total de citas
- Desglose por estado
- Próximas 7 días
- Tendencia mensual

```python
self.assertEqual(data['total_appointments'], 1)
self.assertEqual(data['upcoming_7_days'], 1)
self.assertIn('monthly_trend', data)
```

#### 8. **test_recent_activity**
**Objetivo:** Validar feed de actividad combinado  
**Setup:**
- 1 orden
- 1 cita
**Verificaciones:**
- Ambos tipos presentes
- Campos correctos por tipo
- Orden cronológico

```python
types = [a['type'] for a in data['activities']]
self.assertIn('order', types)
self.assertIn('appointment', types)
```

#### 9. **test_recent_activity_with_limit**
**Objetivo:** Probar parámetro limit  
**Test:** `?limit=5` debe respetar límite

```python
response = self.staff_client.get(f'{self.activity_url}?limit=5')
self.assertLessEqual(len(response.data['activities']), 5)
```

#### 10. **test_low_stock_products**
**Objetivo:** Identificar productos con stock bajo  
**Setup:**
- Producto con stock=5
- Threshold=10
**Resultado:** 1 producto retornado

```python
self.assertEqual(len(data['products']), 1)
self.assertEqual(data['products'][0]['stock'], 5)
```

#### 11. **test_low_stock_custom_threshold**
**Objetivo:** Probar diferentes umbrales  
**Casos:**
- threshold=3 → 0 productos
- threshold=60 → 2 productos (stock 5 y 50)

```python
# Threshold bajo: sin resultados
response = self.staff_client.get(f'{self.low_stock_url}?threshold=3')
self.assertEqual(len(response.data['products']), 0)

# Threshold alto: múltiples resultados
response = self.staff_client.get(f'{self.low_stock_url}?threshold=60')
self.assertEqual(len(response.data['products']), 2)
```

#### 12. **test_all_endpoints_require_staff**
**Objetivo:** Verificar permisos en todos los endpoints  
**Endpoints verificados:**
- /api/dashboard/stats/
- /api/dashboard/sales-over-time/
- /api/dashboard/popular-products/
- /api/dashboard/appointments-stats/
- /api/dashboard/recent-activity/
- /api/dashboard/low-stock/

**Resultado esperado:** 403 Forbidden para usuario regular

```python
endpoints = [
    self.url,
    self.sales_url,
    self.popular_url,
    # ... rest
]
for endpoint in endpoints:
    response = self.client.get(
        endpoint,
        HTTP_AUTHORIZATION=f'Bearer {self.user_token}'
    )
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
```

### Resultados Finales

```
Ran 12 tests in 8.215s
OK

✅ test_all_endpoints_require_staff ... ok
✅ test_appointments_stats ... ok
✅ test_dashboard_stats_requires_staff ... ok
✅ test_dashboard_stats_success ... ok
✅ test_low_stock_custom_threshold ... ok
✅ test_low_stock_products ... ok
✅ test_popular_products ... ok
✅ test_popular_products_with_limit ... ok
✅ test_recent_activity ... ok
✅ test_recent_activity_with_limit ... ok
✅ test_sales_over_time_daily ... ok
✅ test_sales_over_time_with_date_range ... ok
```

---

## 🔐 Seguridad y Permisos

### Implementación

```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        # Solo usuarios con is_staff=True pueden acceder
        ...
```

### Flujo de Autorización

1. **Usuario hace request:** `GET /api/dashboard/stats/`
2. **DRF verifica token:** JWT debe ser válido
3. **IsAuthenticated:** Usuario debe estar autenticado
4. **IsAdminUser:** Usuario debe tener `is_staff=True`
5. **Si falla:** 401 Unauthorized o 403 Forbidden
6. **Si pasa:** Ejecutar view logic

### Crear Usuario Staff

```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@aqpvet.com
# Password: admin123
```

O programáticamente:
```python
from django.contrib.auth.models import User
user = User.objects.create_user(
    username='staff_user',
    password='password123',
    is_staff=True
)
```

---

## 🚀 Optimizaciones

### 1. Queries Eficientes

```python
# ❌ Malo: N+1 queries
orders = Order.objects.all()
for order in orders:
    print(order.user.username)  # Query adicional por cada order

# ✅ Bueno: 1 query con JOIN
orders = Order.objects.select_related('user').all()
for order in orders:
    print(order.user.username)  # Sin queries adicionales
```

### 2. Agregaciones en BD

```python
# ❌ Malo: Calcular en Python
total = sum([order.total_amount for order in orders])

# ✅ Bueno: Agregar en BD
total = orders.aggregate(Sum('total_amount'))['total_amount__sum']
```

### 3. Índices de BD

```python
class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    status = models.CharField(max_length=20, db_index=True)
    # Índices mejoran queries con filtros WHERE y ORDER BY
```

### 4. Caché (futuro)

```python
from django.core.cache import cache

def get_dashboard_stats():
    stats = cache.get('dashboard_stats')
    if stats is None:
        stats = calculate_stats()
        cache.set('dashboard_stats', stats, 300)  # 5 min
    return stats
```

---

## 📊 Métricas de Rendimiento

### Tiempos de Respuesta (Estimados)

| Endpoint | Tiempo | Complejidad |
|----------|--------|-------------|
| /stats/ | ~100ms | 8 queries agregadas |
| /sales-over-time/ | ~50ms | 1 query con TruncDate |
| /popular-products/ | ~30ms | 1 query agregada |
| /appointments-stats/ | ~40ms | 3 queries |
| /recent-activity/ | ~60ms | 2 queries + merge |
| /low-stock/ | ~20ms | 1 query simple |

**Total carga paralela:** ~200-300ms (frontend hace 6 requests simultáneos)

### Escalabilidad

Con 1,000 pedidos:
- Stats: ~150ms
- Sales over time: ~80ms
- Popular products: ~50ms

Con 10,000 pedidos:
- Stats: ~500ms
- Sales over time: ~200ms
- Recomendación: Añadir caché

---

## 🐛 Troubleshooting

### Error: "Cannot resolve keyword 'subtotal'"
**Causa:** Intentar agregar sobre una propiedad (@property)  
**Solución:** Usar F() expressions

```python
# ❌ Malo
Sum('subtotal')

# ✅ Bueno
Sum(F('unit_price') * F('quantity'))
```

### Error: "Appointment() got unexpected keyword 'date'"
**Causa:** Usar nombres de campos incorrectos  
**Solución:** Verificar modelo

```python
# ❌ Malo
Appointment.objects.create(date=..., time=...)

# ✅ Bueno
Appointment.objects.create(appointment_date=..., appointment_time=...)
```

### Error: "403 Forbidden" en dashboard
**Causa:** Usuario no es staff  
**Solución:**
```python
user = User.objects.get(username='tu_usuario')
user.is_staff = True
user.save()
```

---

## 📚 Referencias

- **Django Aggregation:** https://docs.djangoproject.com/en/5.2/topics/db/aggregation/
- **DRF Permissions:** https://www.django-rest-framework.org/api-guide/permissions/
- **TruncDate/Week/Month:** https://docs.djangoproject.com/en/5.2/ref/models/database-functions/#truncdate
- **F() expressions:** https://docs.djangoproject.com/en/5.2/ref/models/expressions/#f-expressions

---

**Última actualización:** Enero 2025  
**Versión:** 1.0.0  
**Estado:** ✅ Producción Ready
