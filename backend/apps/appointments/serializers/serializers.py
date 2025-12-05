from rest_framework import serializers

from apps.appointments.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
	owner_username = serializers.CharField(source='owner.username', read_only=True)
	pet_name = serializers.CharField(source='pet.name', read_only=True)

	class Meta:
		model = Appointment
		fields = [
			'id', 'owner', 'owner_username', 'pet', 'pet_name',
			'scheduled_at', 'reason', 'status', 'notes',
			'created_at', 'updated_at',
		]
		read_only_fields = ['id', 'owner', 'created_at', 'updated_at']


class AppointmentCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Appointment
		fields = ['pet', 'scheduled_at', 'reason', 'status', 'notes']

	def validate(self, attrs):
		request = self.context.get('request')
		if request and not request.user.is_staff:
			pet = attrs.get('pet')
			if pet and pet.owner_id != request.user.id:
				raise serializers.ValidationError('Solo puedes agendar citas para tus mascotas.')
		return attrs
