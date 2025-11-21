from django.urls import path
from apps.memberships.views import MembershipListCreateView, MembershipDetailView

urlpatterns = [
    path('memberships/', MembershipListCreateView.as_view(), name='membership-list-create'),
    path('memberships/<int:pk>/', MembershipDetailView.as_view(), name='membership-detail'),
]
