from rest_framework import generics, permissions
from .models import Pet
from .serializers import PetSerializer

class PetListCreateView(generics.ListCreateAPIView):
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Cada usuario solo ve sus propias mascotas
        return Pet.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        # Al crear, asignar automáticamente al usuario actual
        serializer.save(owner=self.request.user)

class PetDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Cada usuario solo puede acceder a sus propias mascotas
        return Pet.objects.filter(owner=self.request.user)
