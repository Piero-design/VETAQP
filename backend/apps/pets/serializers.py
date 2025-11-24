from rest_framework import serializers
from .models import Pet

class PetSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Pet
        fields = ['id', 'name', 'species', 'age', 'owner', 'owner_name']
        read_only_fields = ['owner']  # El owner se asigna automáticamente
