from django.urls import path
from apps.chat.views import (
    VeterinarianListView,
    ChatRoomListCreateView,
    ChatRoomDetailView,
    ChatMessageListView,
    MarkMessagesAsReadView,
    UnreadMessagesCountView,
)

urlpatterns = [
    path('veterinarians/', VeterinarianListView.as_view(), name='veterinarian-list'),
    path('rooms/', ChatRoomListCreateView.as_view(), name='chatroom-list-create'),
    path('rooms/<int:pk>/', ChatRoomDetailView.as_view(), name='chatroom-detail'),
    path('rooms/<int:room_id>/messages/', ChatMessageListView.as_view(), name='chat-messages'),
    path('rooms/<int:room_id>/mark-as-read/', MarkMessagesAsReadView.as_view(), name='mark-messages-read'),
    path('unread-count/', UnreadMessagesCountView.as_view(), name='unread-count'),
]
