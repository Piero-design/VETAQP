from rest_framework import serializers
from .models import Product, Category, SubCategory, PetType

class PetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetType
        fields = ['id', 'name']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'slug']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    pet_type = PetTypeSerializer(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'pet_type', 'subcategories']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    pet_type = PetTypeSerializer(read_only=True)
    final_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'sku', 'price', 'discount_price',
            'final_price', 'stock', 'brand', 'weight', 'ingredients',
            'image', 'image_url', 'status', 'pet_type', 'category',
            'subcategory', 'created_at', 'updated_at'
        ]
    
    def get_final_price(self, obj):
        return str(obj.get_final_price())
