from django.db import models

class PetType(models.Model):
    PET_CHOICES = [('dog', 'Perro'), ('cat', 'Gato')]
    name = models.CharField(max_length=10, choices=PET_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_name_display()

class Category(models.Model):
    name = models.CharField(max_length=100)
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE, related_name='categories')
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return f"{self.name} ({self.pet_type.get_name_display()})"

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    slug = models.SlugField()
    
    class Meta:
        verbose_name_plural = 'SubCategories'
        unique_together = ('category', 'slug')
    
    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Product(models.Model):
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('inactive', 'Inactivo'),
        ('discontinued', 'Descontinuado')
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=50, unique=True, null=True, blank=True)
    
    pet_type = models.ForeignKey(PetType, on_delete=models.PROTECT, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=5)
    
    brand = models.CharField(max_length=100, blank=True)
    weight = models.CharField(max_length=50, blank=True)
    ingredients = models.TextField(blank=True)
    
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['pet_type', 'category']),
            models.Index(fields=['status', 'stock']),
        ]
    
    def __str__(self):
        return self.name
    
    def is_in_stock(self):
        return self.stock > 0
    
    def is_low_stock(self):
        return 0 < self.stock <= self.low_stock_threshold
    
    def get_final_price(self):
        return self.discount_price if self.discount_price else self.price
