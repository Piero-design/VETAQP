from django.urls import path
from apps.notifications.views.views import index

urlpatterns = [
    path('', index, name='notifications_index'),
]
