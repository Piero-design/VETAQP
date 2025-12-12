from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    # Imagen subida desde el backend (puede quedar vacío)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    # Imagen desde URL externa (Unsplash, Picsum, etc.)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
