from rest_framework import generics, permissions
from .models import Pet
from .serializers import PetSerializer

class PetListCreateView(generics.ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
