from rest_framework import serializers
from apps.memberships.models import Membership
from datetime import timedelta


class MembershipSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    plan_name_display = serializers.CharField(source='get_plan_name_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    days_remaining = serializers.IntegerField(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Membership
        fields = [
            'id', 'user', 'user_username', 'plan_name', 'plan_name_display',
            'status', 'status_display', 'start_date', 'end_date', 'price',
            'auto_renew', 'notes', 'days_remaining', 'is_expired',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'status', 'created_at', 'updated_at']


class MembershipCreateSerializer(serializers.ModelSerializer):
    duration_days = serializers.IntegerField(write_only=True, required=False, default=30)
    
    class Meta:
        model = Membership
        fields = ['plan_name', 'price', 'auto_renew', 'notes', 'duration_days']
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a cero.")
        return value
    
    def create(self, validated_data):
        duration_days = validated_data.pop('duration_days', 30)
        
        # Calcular end_date basado en duración
        from django.utils import timezone
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=duration_days)
        
        validated_data['start_date'] = start_date
        validated_data['end_date'] = end_date
        
        return super().create(validated_data)
