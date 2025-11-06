from django.urls import path
from apps.payments.views.views import index

urlpatterns = [
    path('', index, name='payments_index'),
]
