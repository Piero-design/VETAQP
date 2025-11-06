from django.urls import path
from apps.pets.views.views import index

urlpatterns = [
    path('', index, name='pets_index'),
]
