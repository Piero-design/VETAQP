from django.urls import path
from apps.notifications.views import (
    NotificationListCreateView,
    NotificationDetailView,
    MarkAsReadView,
    MarkAllAsReadView,
    UnreadCountView,
)

urlpatterns = [
    path('', NotificationListCreateView.as_view(), name='notification-list-create'),
    path('<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('<int:pk>/mark-as-read/', MarkAsReadView.as_view(), name='notification-mark-as-read'),
    path('mark-all-as-read/', MarkAllAsReadView.as_view(), name='notification-mark-all-as-read'),
    path('unread-count/', UnreadCountView.as_view(), name='notification-unread-count'),
]
