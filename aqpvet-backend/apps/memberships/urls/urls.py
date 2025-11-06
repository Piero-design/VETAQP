from django.urls import path
from apps.memberships.views.views import index

urlpatterns = [
    path('', index, name='memberships_index'),
]
