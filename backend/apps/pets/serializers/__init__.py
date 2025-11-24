from rest_framework import serializers
from apps.pets.models import Pet, MedicalRecord, Vaccine
from django.contrib.auth.models import User


class PetSerializer(serializers.ModelSerializer):
    """Serializer original para Pet (CRUD básico)"""
    class Meta:
        model = Pet
        fields = '__all__'


class PetMinimalSerializer(serializers.ModelSerializer):
    """Serializer simplificado para Pet"""
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Pet
        fields = ['id', 'name', 'species', 'age', 'owner', 'owner_username']
        read_only_fields = ['id']


class MedicalRecordSerializer(serializers.ModelSerializer):
    """Serializer para registros médicos"""
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    pet_species = serializers.CharField(source='pet.species', read_only=True)
    owner_username = serializers.CharField(source='pet.owner.username', read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'pet', 'pet_name', 'pet_species', 'owner_username',
            'date', 'diagnosis', 'treatment', 'veterinarian',
            'notes', 'weight', 'temperature', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_pet(self, value):
        """Validar que el usuario tiene acceso a la mascota"""
        user = self.context['request'].user
        # Staff puede crear registros para cualquier mascota
        if user.is_staff:
            return value
        # Usuarios normales solo pueden ver sus propias mascotas
        if value.owner != user:
            raise serializers.ValidationError("No tienes permiso para crear registros para esta mascota.")
        return value


class VaccineSerializer(serializers.ModelSerializer):
    """Serializer para vacunas"""
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    pet_species = serializers.CharField(source='pet.species', read_only=True)
    owner_username = serializers.CharField(source='pet.owner.username', read_only=True)
    is_next_dose_pending = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Vaccine
        fields = [
            'id', 'pet', 'pet_name', 'pet_species', 'owner_username',
            'vaccine_name', 'date_administered', 'next_dose_date',
            'veterinarian', 'batch_number', 'notes', 'is_next_dose_pending', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_pet(self, value):
        """Validar que el usuario tiene acceso a la mascota"""
        user = self.context['request'].user
        # Staff puede crear vacunas para cualquier mascota
        if user.is_staff:
            return value
        # Usuarios normales solo pueden ver sus propias mascotas
        if value.owner != user:
            raise serializers.ValidationError("No tienes permiso para crear vacunas para esta mascota.")
        return value
    
    def validate(self, data):
        """Validar que next_dose_date sea posterior a date_administered"""
        if data.get('next_dose_date') and data.get('date_administered'):
            if data['next_dose_date'] < data['date_administered']:
                raise serializers.ValidationError({
                    "next_dose_date": "La fecha de la próxima dosis no puede ser anterior a la fecha de aplicación."
                })
        return data


class PetDetailSerializer(serializers.ModelSerializer):
    """Serializer completo para Pet con historial médico"""
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    medical_records = MedicalRecordSerializer(many=True, read_only=True)
    vaccines = VaccineSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'species', 'age', 'owner', 'owner_username', 'owner_email',
            'medical_records', 'vaccines'
        ]
        read_only_fields = ['id']
