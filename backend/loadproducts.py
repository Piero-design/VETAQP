from apps.products.models import Product

PRODUCTS_DATA = [
    # Productos para perro
    {
        "name": "Croquetas premium perro 2kg",
        "description": "Alimento completo para perro adulto de raza mediana.",
        "price": 79.90,
        "stock": 25,
        "image_url": "https://images.unsplash.com/photo-1583512603705-142cf556bbd1",
    },
    {
        "name": "Croquetas cachorro 1kg",
        "description": "Fórmula especial para cachorros en crecimiento.",
        "price": 49.90,
        "stock": 30,
        "image_url": "https://images.unsplash.com/photo-1606787366850-de6330128bfc",
    },

    # Productos para gato
    {
        "name": "Alimento seco gato adulto 2kg",
        "description": "Alimento balanceado para gato adulto.",
        "price": 69.90,
        "stock": 20,
        "image_url": "https://images.unsplash.com/photo-1518791841217-8f162f1e1131",
    },
    {
        "name": "Snacks para gato",
        "description": "Snacks crocantes con sabor a pollo.",
        "price": 17.50,
        "stock": 45,
        "image_url": "https://images.unsplash.com/photo-1543852786-1cf6624b9987",
    },

    # Juguetes
    {
        "name": "Pelota de goma para perro",
        "description": "Resistente, ideal para juegos al aire libre.",
        "price": 15.90,
        "stock": 60,
        "image_url": "https://images.unsplash.com/photo-1517423440428-a5a00ad493e8",
    },

    # Higiene
    {
        "name": "Shampoo para perro piel sensible",
        "description": "Ideal para perros con piel delicada.",
        "price": 29.90,
        "stock": 18,
        "image_url": "https://images.unsplash.com/photo-1603394266923-8f756150d3e0",
    },

    # Accesorios
    {
        "name": "Collar ajustable para perro",
        "description": "Collar de nylon resistente con hebilla metálica.",
        "price": 25.90,
        "stock": 40,
        "image_url": "https://images.unsplash.com/photo-1507149833265-60c372daea22",
    },
]

# 20 productos aleatorios de Picsum
for i in range(1, 21):
    PRODUCTS_DATA.append({
        "name": f"Producto Genérico {i}",
        "description": "Producto de demostración para catálogo.",
        "price": 10 + i,
        "stock": 10 + i,
        "image_url": f"https://picsum.photos/400/400?random={i}"
    })


def run():
    total = 0
    for data in PRODUCTS_DATA:
        obj, created = Product.objects.get_or_create(
            name=data["name"],
            defaults=data,
        )
        if created:
            total += 1
    print(f"Se crearon {total} productos.")
