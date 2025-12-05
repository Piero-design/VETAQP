from rest_framework import serializers

from apps.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
	customer_username = serializers.CharField(source='customer.username', read_only=True)

	class Meta:
		model = Order
		fields = [
			'id', 'customer', 'customer_username', 'total',
			'status', 'notes', 'created_at', 'updated_at',
		]
		read_only_fields = ['id', 'customer', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = ['total', 'status', 'notes']

	def validate_total(self, value):
		if value <= 0:
			raise serializers.ValidationError('El total debe ser mayor a cero.')
		return value
