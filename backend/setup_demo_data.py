"""
Script para crear datos de demostración en AQPVET
- 3 usuarios regulares con mascotas e historial
- 1 usuario admin para dashboard
- Productos en catálogo
- Pedidos y citas
"""
import os
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aqpvet.settings')
django.setup()

from django.contrib.auth.models import User
from apps.pets.models import Pet, MedicalRecord, Vaccine
from apps.products.models import Product
from apps.orders.models import Order, OrderItem
from apps.appointments.models import Appointment
from apps.payments.models import Payment

print("🚀 Creando datos de demostración para AQPVET...\n")

# =============================================================================
# 1. CREAR USUARIOS
# =============================================================================
print("👥 Creando usuarios...")

# Usuario Admin para Dashboard
admin, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@aqpvet.com',
        'first_name': 'Admin',
        'last_name': 'AQPVET',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    admin.set_password('admin123')
    admin.save()
    print(f"  ✅ Admin creado: admin / admin123")
else:
    print(f"  ℹ️  Admin ya existe: admin")

# Usuarios regulares
usuarios_data = [
    {
        'username': 'juan.perez',
        'email': 'juan.perez@email.com',
        'first_name': 'Juan',
        'last_name': 'Pérez',
        'password': 'pass123'
    },
    {
        'username': 'maria.garcia',
        'email': 'maria.garcia@email.com',
        'first_name': 'María',
        'last_name': 'García',
        'password': 'pass123'
    },
    {
        'username': 'carlos.lopez',
        'email': 'carlos.lopez@email.com',
        'first_name': 'Carlos',
        'last_name': 'López',
        'password': 'pass123'
    }
]

usuarios = []
for user_data in usuarios_data:
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={
            'email': user_data['email'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name']
        }
    )
    if created:
        user.set_password(user_data['password'])
        user.save()
        print(f"  ✅ Usuario creado: {user.username} / pass123")
    else:
        print(f"  ℹ️  Usuario ya existe: {user.username}")
    usuarios.append(user)

# =============================================================================
# 2. CREAR PRODUCTOS (sin categorías)
# =============================================================================
print("\n📦 Creando productos...")

productos_data = [
    # Alimentos
    ('Alimento Premium Adulto 15kg', 125.00, 50, 'Alimento balanceado para perros adultos'),
    ('Alimento Cachorros 10kg', 95.00, 40, 'Nutrición completa para cachorros'),
    ('Alimento Gatos Adultos 7.5kg', 85.00, 35, 'Alimento premium para gatos'),
    
    # Accesorios
    ('Collar Antipulgas', 25.00, 100, 'Protección contra pulgas y garrapatas'),
    ('Correa Extensible 5m', 45.00, 60, 'Correa retráctil de alta resistencia'),
    ('Cama para Mascotas Grande', 120.00, 25, 'Cama acolchada y lavable'),
    
    # Higiene
    ('Shampoo Medicado 500ml', 35.00, 80, 'Shampoo antiséptico veterinario'),
    ('Cepillo Dental + Pasta', 28.00, 70, 'Kit completo de higiene dental'),
    ('Toallitas Húmedas x50', 15.00, 120, 'Toallitas para limpieza diaria'),
    
    # Medicamentos
    ('Desparasitante Interno', 42.00, 90, 'Tabletas antiparasitarias'),
    ('Vitaminas Multiples', 38.00, 75, 'Suplemento vitamínico completo'),
    ('Antipulgas Spot-On', 55.00, 85, 'Tratamiento tópico antipulgas'),
    
    # Juguetes
    ('Pelota Kong Resistente', 32.00, 110, 'Juguete indestructible para perros'),
    ('Ratón con Catnip', 12.00, 150, 'Juguete para gatos con hierba gatera'),
    ('Cuerda para Jalar', 18.00, 95, 'Juguete interactivo para perros'),
]

productos = []
for nombre, precio, stock, desc in productos_data:
    producto, created = Product.objects.get_or_create(
        name=nombre,
        defaults={
            'price': Decimal(str(precio)),
            'stock': stock,
            'description': desc
        }
    )
    if created:
        print(f"  ✅ Producto: {nombre} - S/ {precio}")
    productos.append(producto)

# =============================================================================
# 3. CREAR MASCOTAS
# =============================================================================
print("\n🐾 Creando mascotas...")

mascotas_data = [
    # Usuario 1: Juan Pérez
    (usuarios[0], 'Max', 'Perro', 5),
    (usuarios[0], 'Luna', 'Gato', 3),
    
    # Usuario 2: María García
    (usuarios[1], 'Rocky', 'Perro', 4),
    
    # Usuario 3: Carlos López
    (usuarios[2], 'Michi', 'Gato', 2),
    (usuarios[2], 'Toby', 'Perro', 6),
]

mascotas = []
for owner, nombre, especie, edad in mascotas_data:
    mascota, created = Pet.objects.get_or_create(
        owner=owner,
        name=nombre,
        defaults={
            'species': especie,
            'age': edad
        }
    )
    if created:
        print(f"  ✅ Mascota: {nombre} ({especie}, {edad} años) - Dueño: {owner.username}")
    mascotas.append(mascota)

# =============================================================================
# 4. CREAR HISTORIAL MÉDICO Y VACUNAS
# =============================================================================
print("\n🏥 Creando historial médico...")

# Registros médicos
registros_data = [
    (mascotas[0], 'Chequeo general', 'Control de rutina, estado saludable', 'Dr. Rodríguez', -30),
    (mascotas[0], 'Vacunación anual', 'Aplicación de vacuna antirrábica', 'Dr. Rodríguez', -15),
    (mascotas[1], 'Consulta por alergias', 'Tratamiento para alergia cutánea', 'Dra. Sánchez', -20),
    (mascotas[2], 'Chequeo general', 'Revisión completa, buen estado', 'Dr. Rodríguez', -45),
    (mascotas[3], 'Limpieza dental', 'Profilaxis dental completa', 'Dra. Torres', -25),
    (mascotas[4], 'Vacunación', 'Refuerzo de vacunas', 'Dr. Rodríguez', -10),
]

for mascota, diagnostico, tratamiento, veterinario, dias_atras in registros_data:
    fecha = datetime.now().date() + timedelta(days=dias_atras)
    record, created = MedicalRecord.objects.get_or_create(
        pet=mascota,
        diagnosis=diagnostico,
        date=fecha,
        defaults={
            'treatment': tratamiento,
            'veterinarian': veterinario,
            'notes': 'Registro generado automáticamente'
        }
    )
    if created:
        print(f"  ✅ Registro: {mascota.name} - {diagnostico}")

# Vacunas
vacunas_data = [
    (mascotas[0], 'Antirrábica', -90, 365),
    (mascotas[0], 'Séxtuple', -180, 365),
    (mascotas[1], 'Triple Felina', -120, 365),
    (mascotas[2], 'Antirrábica', -60, 365),
    (mascotas[4], 'Antirrábica', -45, 365),
]

for mascota, nombre, dias_aplicacion, dias_siguiente in vacunas_data:
    fecha_aplicacion = datetime.now().date() + timedelta(days=dias_aplicacion)
    fecha_siguiente = fecha_aplicacion + timedelta(days=dias_siguiente)
    
    vaccine, created = Vaccine.objects.get_or_create(
        pet=mascota,
        vaccine_name=nombre,
        date_administered=fecha_aplicacion,
        defaults={
            'next_dose_date': fecha_siguiente,
            'veterinarian': 'Dr. Rodríguez',
            'notes': 'Vacuna aplicada correctamente'
        }
    )
    if created:
        print(f"  ✅ Vacuna: {mascota.name} - {nombre}")

# =============================================================================
# 5. CREAR PEDIDOS Y PAGOS
# =============================================================================
print("\n🛒 Creando pedidos...")

pedidos_data = [
    # (usuario, productos[(producto_idx, cantidad)], estado, dias_atras)
    (usuarios[0], [(0, 1), (3, 2)], 'DELIVERED', -45),  # Juan - Alimento + Collares
    (usuarios[0], [(6, 1), (7, 1)], 'DELIVERED', -30),  # Juan - Shampoo + Cepillo
    (usuarios[0], [(12, 2)], 'PROCESSING', -3),         # Juan - Pelotas
    
    (usuarios[1], [(1, 1), (4, 1)], 'DELIVERED', -60),  # María - Alimento + Correa
    (usuarios[1], [(9, 1), (10, 1)], 'SHIPPED', -5),    # María - Desparasitante + Vitaminas
    
    (usuarios[2], [(2, 1), (5, 1)], 'DELIVERED', -50),  # Carlos - Alimento gatos + Cama
    (usuarios[2], [(8, 3), (13, 2)], 'DELIVERED', -25), # Carlos - Toallitas + Ratones
    (usuarios[2], [(11, 1)], 'PENDING', -1),            # Carlos - Antipulgas
]

for usuario, items, estado, dias_atras in pedidos_data:
    fecha_pedido = datetime.now() - timedelta(days=abs(dias_atras))
    
    # Calcular total
    total = sum(productos[prod_idx].price * cantidad for prod_idx, cantidad in items)
    
    # Crear orden
    order = Order.objects.create(
        user=usuario,
        status=estado,
        shipping_status='DELIVERED' if estado == 'DELIVERED' else ('SHIPPED' if estado == 'SHIPPED' else 'PENDING'),
        total=total,
        shipping_address=f'{usuario.first_name} {usuario.last_name}, Calle Principal 123, Arequipa'
    )
    # Actualizar created_at manualmente
    Order.objects.filter(id=order.id).update(created_at=fecha_pedido)
    
    # Crear items del pedido
    for prod_idx, cantidad in items:
        producto = productos[prod_idx]
        OrderItem.objects.create(
            order=order,
            product=producto,
            quantity=cantidad,
            unit_price=producto.price
        )
    
    # Crear pago
    payment = Payment.objects.create(
        user=usuario,
        order=order,
        amount=total,
        payment_method='CARD' if usuario.id % 2 == 0 else 'YAPE',
        status='COMPLETED' if estado != 'PENDING' else 'PENDING',
        transaction_id=f'TXN{order.id}{usuario.id}'
    )
    # Actualizar created_at manualmente
    Payment.objects.filter(id=payment.id).update(created_at=fecha_pedido)
    
    print(f"  ✅ Pedido #{order.id}: {usuario.username} - S/ {total} ({estado})")

# =============================================================================
# 6. CREAR CITAS
# =============================================================================
print("\n📅 Creando citas...")

citas_data = [
    # (usuario, mascota_idx, motivo, estado, dias_offset)
    (usuarios[0], 0, 'Consulta general', 'COMPLETED', -20),     # Max - pasada
    (usuarios[0], 1, 'Vacunación', 'COMPLETED', -15),           # Luna - pasada
    (usuarios[0], 0, 'Control de peso', 'SCHEDULED', 5),        # Max - futura
    
    (usuarios[1], 2, 'Chequeo anual', 'COMPLETED', -30),        # Rocky - pasada
    (usuarios[1], 2, 'Consulta por cojera', 'CONFIRMED', 3),    # Rocky - futura
    
    (usuarios[2], 3, 'Peluquería', 'COMPLETED', -10),           # Michi - pasada
    (usuarios[2], 4, 'Vacunación', 'SCHEDULED', 7),             # Toby - futura
]

citas = []
for usuario, mascota_idx, motivo, estado, dias_offset in citas_data:
    fecha_cita = datetime.now().date() + timedelta(days=dias_offset)
    hora_cita = datetime.now().time().replace(hour=10, minute=0, second=0, microsecond=0)
    
    # Encontrar la mascota correcta del usuario
    mascota = [m for m in mascotas if m.owner == usuario][mascota_idx if mascota_idx < len([m for m in mascotas if m.owner == usuario]) else 0]
    
    appointment = Appointment.objects.create(
        user=usuario,
        pet=mascota,
        appointment_date=fecha_cita,
        appointment_time=hora_cita,
        reason=motivo,
        status=estado,
        veterinarian='Dr. Rodríguez' if dias_offset < 0 else 'Dr. Sánchez'
    )
    citas.append(appointment)
    print(f"  ✅ Cita #{appointment.id}: {mascota.name} - {motivo} ({estado})")

# =============================================================================
# RESUMEN FINAL
# =============================================================================
print("\n" + "="*60)
print("✅ DATOS DE DEMOSTRACIÓN CREADOS EXITOSAMENTE")
print("="*60)

print(f"\n👥 USUARIOS CREADOS:")
print(f"   🔑 Admin Dashboard: admin / admin123")
print(f"   👤 Usuario 1: juan.perez / pass123")
print(f"   👤 Usuario 2: maria.garcia / pass123")
print(f"   👤 Usuario 3: carlos.lopez / pass123")

print(f"\n📊 ESTADÍSTICAS:")
print(f"   • Usuarios: {User.objects.count()}")
print(f"   • Productos: {Product.objects.count()}")
print(f"   • Mascotas: {Pet.objects.count()}")
print(f"   • Pedidos: {Order.objects.count()}")
print(f"   • Citas: {Appointment.objects.count()}")
print(f"   • Registros Médicos: {MedicalRecord.objects.count()}")
print(f"   • Vacunas: {Vaccine.objects.count()}")
print(f"   • Pagos: {Payment.objects.count()}")

print(f"\n🌐 ACCESOS:")
print(f"   • Backend: http://localhost:8000")
print(f"   • Frontend: http://localhost:5173")
print(f"   • Dashboard: http://localhost:5173/dashboard (login: admin/admin123)")
print(f"   • Admin Panel: http://localhost:8000/admin (login: admin/admin123)")

print("\n🚀 ¡Sistema listo para usar!")
