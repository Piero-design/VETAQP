from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from apps.memberships.models import Membership
from apps.memberships.serializers import MembershipSerializer, MembershipCreateSerializer


class MembershipListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'plan_name', 'auto_renew']
    ordering_fields = ['created_at', 'end_date', 'price']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Los usuarios ven solo sus membresías, admins ven todas
        if self.request.user.is_staff:
            return Membership.objects.all()
        return Membership.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MembershipCreateSerializer
        return MembershipSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MembershipDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MembershipSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Membership.objects.all()
        return Membership.objects.filter(user=self.request.user)
