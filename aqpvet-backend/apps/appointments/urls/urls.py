from django.urls import path
from apps.appointments.views.views import index

urlpatterns = [
    path('', index, name='appointments_index'),
]
