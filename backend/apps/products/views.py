from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category, PetType
from .serializers import ProductSerializer, CategorySerializer, PetTypeSerializer

class PetTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PetType.objects.all()
    serializer_class = PetTypeSerializer
    permission_classes = [permissions.AllowAny]

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ['pet_type']

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(status='active')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['pet_type', 'category', 'subcategory']
    search_fields = ['name', 'description', 'brand']
    ordering_fields = ['price', 'created_at', 'stock']
    ordering = ['-created_at']
