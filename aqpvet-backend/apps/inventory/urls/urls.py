from django.urls import path
from apps.inventory.views.views import index

urlpatterns = [
    path('', index, name='inventory_index'),
]
