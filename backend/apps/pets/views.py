from rest_framework import generics, permissions

from .models import Pet
from .serializers import PetSerializer


class PetListCreateView(generics.ListCreateAPIView):
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Pet.objects.all()
        return Pet.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PetDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Pet.objects.all()
        return Pet.objects.filter(owner=user)
