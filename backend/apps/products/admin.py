from django.contrib import admin
from .models import PetType, Category, SubCategory, Product

@admin.register(PetType)
class PetTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'pet_type', 'slug']
    list_filter = ['pet_type']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug']
    list_filter = ['category']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'pet_type', 'category', 'price', 'stock', 'status']
    list_filter = ['status', 'pet_type', 'category', 'created_at']
    search_fields = ['name', 'sku', 'brand']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'description', 'sku', 'status')
        }),
        ('Categorización', {
            'fields': ('pet_type', 'category', 'subcategory')
        }),
        ('Precios', {
            'fields': ('price', 'discount_price')
        }),
        ('Stock', {
            'fields': ('stock', 'low_stock_threshold')
        }),
        ('Detalles del producto', {
            'fields': ('brand', 'weight', 'ingredients')
        }),
        ('Imágenes', {
            'fields': ('image', 'image_url')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
