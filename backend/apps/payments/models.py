from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Payment(models.Model):
	METHOD_CASH = 'CASH'
	METHOD_CARD = 'CARD'
	METHOD_TRANSFER = 'TRANSFER'
	METHOD_YAPE = 'YAPE'

	METHOD_CHOICES = (
		(METHOD_CASH, 'Efectivo'),
		(METHOD_CARD, 'Tarjeta'),
		(METHOD_TRANSFER, 'Transferencia Bancaria'),
		(METHOD_YAPE, 'Yape/Plin'),
	)

	STATUS_PENDING = 'PENDING'
	STATUS_COMPLETED = 'COMPLETED'
	STATUS_FAILED = 'FAILED'
	STATUS_REFUNDED = 'REFUNDED'

	STATUS_CHOICES = (
		(STATUS_PENDING, 'Pendiente'),
		(STATUS_COMPLETED, 'Completado'),
		(STATUS_FAILED, 'Fallido'),
		(STATUS_REFUNDED, 'Reembolsado'),
	)

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
	transaction_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"Pago {self.id} - {self.user.username} - {self.amount}"
