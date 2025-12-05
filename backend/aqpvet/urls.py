from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth JWT
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Módulos principales
    path('api/users/', include('apps.users.urls')),
    path('api/pets/', include('apps.pets.urls')),
    path('api/products/', include('apps.products.urls')),
    path('api/inventory/', include('apps.inventory.urls.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/appointments/', include('apps.appointments.urls')),
    path('api/', include('apps.payments.urls.urls')),
    path('api/', include('apps.memberships.urls.urls')),
    path('api/', include('apps.orders.urls')),
    path('api/', include('apps.appointments.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/chat/', include('apps.chat.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
]
