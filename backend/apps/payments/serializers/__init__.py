from rest_framework import serializers
from apps.payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    # order_id = serializers.IntegerField(source='order.id', read_only=True, allow_null=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'user_username', 'amount', 
            'payment_method', 'payment_method_display', 'status', 'status_display',
            'transaction_id', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method', 'transaction_id', 'notes']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a cero.")
        return value
