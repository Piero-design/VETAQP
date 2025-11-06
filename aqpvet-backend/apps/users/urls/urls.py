from django.urls import path
from apps.users.views.views import index

urlpatterns = [
    path('', index, name='users_index'),
]
