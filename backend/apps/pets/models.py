from django.db import models
from django.contrib.auth.models import User

class Pet(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')

    def __str__(self):
        return self.name
