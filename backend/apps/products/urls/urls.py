from django.urls import path
from apps.products.views.views import index

urlpatterns = [
    path('', index, name='products_index'),
]
