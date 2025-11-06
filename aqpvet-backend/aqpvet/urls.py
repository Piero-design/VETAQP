from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas de cada módulo del backend
    path('api/users/', include('apps.users.urls.urls')),
    path('api/pets/', include('apps.pets.urls.urls')),
    path('api/products/', include('apps.products.urls.urls')),
    path('api/orders/', include('apps.orders.urls.urls')),
    path('api/payments/', include('apps.payments.urls.urls')),
    path('api/appointments/', include('apps.appointments.urls.urls')),
    path('api/notifications/', include('apps.notifications.urls.urls')),
    path('api/inventory/', include('apps.inventory.urls.urls')),
    path('api/memberships/', include('apps.memberships.urls.urls')),
]
