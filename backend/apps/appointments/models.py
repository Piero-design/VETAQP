from django.db import models
from django.contrib.auth import get_user_model

from apps.pets.models import Pet

User = get_user_model()


class Appointment(models.Model):
	STATUS_SCHEDULED = 'scheduled'
	STATUS_COMPLETED = 'completed'
	STATUS_CANCELLED = 'cancelled'

	STATUS_CHOICES = (
		(STATUS_SCHEDULED, 'Scheduled'),
		(STATUS_COMPLETED, 'Completed'),
		(STATUS_CANCELLED, 'Cancelled'),
	)

	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
	pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='appointments')
	scheduled_at = models.DateTimeField()
	reason = models.CharField(max_length=255)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_SCHEDULED)
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-scheduled_at']

	def __str__(self):
		return f"{self.pet.name} - {self.scheduled_at:%Y-%m-%d %H:%M}"
