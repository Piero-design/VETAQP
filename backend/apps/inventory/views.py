from rest_framework import generics, permissions
from .models import StockMovement
from .serializers import StockMovementSerializer


class StockMovementListCreateView(generics.ListCreateAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StockMovementDetailView(generics.RetrieveAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [permissions.IsAuthenticated]
