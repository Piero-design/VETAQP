from django.urls import path
from apps.orders.views.views import index

urlpatterns = [
    path('', index, name='orders_index'),
]
