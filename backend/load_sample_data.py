import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aqpvet.settings')
django.setup()

from apps.products.models import PetType, Category, SubCategory, Product
from django.contrib.auth.models import User

def create_sample_data():
    print("Creando datos de ejemplo...")
    
    # Crear tipos de mascota
    dog, _ = PetType.objects.get_or_create(name='dog')
    cat, _ = PetType.objects.get_or_create(name='cat')
    print("✓ Tipos de mascota creados")
    
    # Crear categorías para perros
    food_dog, _ = Category.objects.get_or_create(
        name='Alimentos',
        pet_type=dog,
        defaults={'slug': 'alimentos-perros', 'icon': 'food'}
    )
    hygiene_dog, _ = Category.objects.get_or_create(
        name='Higiene y Cuidado',
        pet_type=dog,
        defaults={'slug': 'higiene-perros', 'icon': 'hygiene'}
    )
    toys_dog, _ = Category.objects.get_or_create(
        name='Juguetes',
        pet_type=dog,
        defaults={'slug': 'juguetes-perros', 'icon': 'toys'}
    )
    
    # Crear categorías para gatos
    food_cat, _ = Category.objects.get_or_create(
        name='Alimentos',
        pet_type=cat,
        defaults={'slug': 'alimentos-gatos', 'icon': 'food'}
    )
    hygiene_cat, _ = Category.objects.get_or_create(
        name='Higiene y Cuidado',
        pet_type=cat,
        defaults={'slug': 'higiene-gatos', 'icon': 'hygiene'}
    )
    
    print("✓ Categorías creadas")
    
    # Crear subcategorías
    SubCategory.objects.get_or_create(
        name='Alimento seco',
        category=food_dog,
        defaults={'slug': 'alimento-seco'}
    )
    SubCategory.objects.get_or_create(
        name='Alimento húmedo',
        category=food_dog,
        defaults={'slug': 'alimento-humedo'}
    )
    SubCategory.objects.get_or_create(
        name='Snacks y premios',
        category=food_dog,
        defaults={'slug': 'snacks-premios'}
    )
    
    print("✓ Subcategorías creadas")
    
    # Crear productos de ejemplo
    products_data = [
        {
            'name': 'Alimento Premium Perro 25kg',
            'description': 'Alimento seco de alta calidad para perros adultos',
            'sku': 'FOOD-DOG-001',
            'pet_type': dog,
            'category': food_dog,
            'price': 120.00,
            'discount_price': 99.99,
            'stock': 50,
            'brand': 'Royal Canin',
            'weight': '25kg',
            'image_url': 'https://images.unsplash.com/photo-1568152950566-c1bf43f0a86d?w=400'
        },
        {
            'name': 'Juguete Kong Resistente',
            'description': 'Juguete de goma resistente para perros',
            'sku': 'TOY-DOG-001',
            'pet_type': dog,
            'category': toys_dog,
            'price': 45.00,
            'discount_price': None,
            'stock': 100,
            'brand': 'Kong',
            'image_url': 'https://images.unsplash.com/photo-1535241749838-299277b6305f?w=400'
        },
        {
            'name': 'Champú Hipoalergénico Perro',
            'description': 'Champú suave para pieles sensibles',
            'sku': 'HYGIENE-DOG-001',
            'pet_type': dog,
            'category': hygiene_dog,
            'price': 35.00,
            'discount_price': 28.00,
            'stock': 75,
            'brand': 'Tropiclean',
            'weight': '473ml',
            'image_url': 'https://images.unsplash.com/photo-1585110396000-c9ffd4d4b3f4?w=400'
        },
        {
            'name': 'Alimento Gato Adulto 7kg',
            'description': 'Alimento completo y balanceado para gatos',
            'sku': 'FOOD-CAT-001',
            'pet_type': cat,
            'category': food_cat,
            'price': 85.00,
            'discount_price': 69.99,
            'stock': 40,
            'brand': 'Purina Pro Plan',
            'weight': '7kg',
            'image_url': 'https://images.unsplash.com/photo-1589941013453-ec89f33b5e95?w=400'
        },
        {
            'name': 'Juguete Pluma Gato',
            'description': 'Juguete interactivo con plumas para gatos',
            'sku': 'TOY-CAT-001',
            'pet_type': cat,
            'category': toys_dog,
            'price': 25.00,
            'discount_price': None,
            'stock': 120,
            'brand': 'Petstages',
            'image_url': 'https://images.unsplash.com/photo-1570158268183-d296b2c5b203?w=400'
        },
    ]
    
    for data in products_data:
        Product.objects.get_or_create(
            sku=data['sku'],
            defaults=data
        )
    
    print(f"✓ {len(products_data)} productos creados")
    print("\n✅ Datos de ejemplo cargados exitosamente")

if __name__ == '__main__':
    create_sample_data()
