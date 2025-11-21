"""
ERRORES DE INTEGRACIÓN INTENCIONALES
Estos errores ocurren en la interacción entre componentes/módulos del sistema.
"""

import sys
import os
# Agregar el directorio padre al path para poder importar los modelos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aqpvet.settings')
import django
django.setup()

from apps.payments.models import Payment
from apps.inventory.models import StockMovement
from apps.products.models import Product
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()


# ERROR DE INTEGRACIÓN #1: Crear pago sin usuario autenticado
# BUG: Intenta crear un pago sin asignar el usuario requerido
def create_payment_without_user(amount, payment_method):
    """
    Intenta crear un pago sin usuario (campo requerido).
    
    Args:
        amount: Monto del pago
        payment_method: Método de pago
    
    CASO DE USO PARA DEBUGGING:
    1. Establecer breakpoint en línea 52
    2. Llamar: create_payment_without_user(100, 'CASH')
    3. Inspeccionar las variables amount y payment_method
    4. Avanzar paso a paso hasta payment.save()
    5. Ver IntegrityError: el campo 'user' no puede ser NULL
    """
    print(f"[DEBUG] Creando pago sin usuario...")
    print(f"[DEBUG] Monto: ${amount}")
    print(f"[DEBUG] Método: {payment_method}")
    
    # BUG INTENCIONAL: no asigna el usuario requerido
    payment = Payment(
        # user=user,  # ❌ FALTA: campo requerido
        amount=Decimal(str(amount)),
        payment_method=payment_method,
        status='PENDING'
    )
    
    print(f"[DEBUG] Guardando pago...")
    payment.save()  # ❌ IntegrityError: NOT NULL constraint failed
    
    print(f"[DEBUG] Pago creado: {payment.id}")
    return payment
    
    # CORRECCIÓN:
    # user = User.objects.first()  # o el usuario autenticado
    # payment = Payment(user=user, amount=..., ...)


# ERROR DE INTEGRACIÓN #2: Actualizar stock con producto inexistente
# BUG: Intenta crear movimiento de stock para producto que no existe
def update_stock_for_nonexistent_product(product_id, quantity):
    """
    Intenta crear movimiento de stock para producto inexistente.
    
    Args:
        product_id: ID del producto (que no existe)
        quantity: Cantidad del movimiento
    
    CASO DE USO PARA DEBUGGING:
    1. Establecer breakpoint en línea 95
    2. Llamar: update_stock_for_nonexistent_product(99999, 10)
    3. Inspeccionar product_id y quantity
    4. Avanzar hasta Product.objects.get()
    5. Ver DoesNotExist: Product matching query does not exist
    """
    print(f"[DEBUG] Actualizando stock...")
    print(f"[DEBUG] Product ID: {product_id}")
    print(f"[DEBUG] Cantidad: {quantity}")
    
    # BUG INTENCIONAL: no valida si el producto existe
    product = Product.objects.get(id=product_id)  # ❌ DoesNotExist si no existe
    
    user = User.objects.first()
    
    movement = StockMovement.objects.create(
        product=product,
        user=user,
        movement_type='IN',
        quantity=quantity,
        reason='Reposición automática'
    )
    
    print(f"[DEBUG] Movimiento creado: {movement.id}")
    return movement
    
    # CORRECCIÓN:
    # try:
    #     product = Product.objects.get(id=product_id)
    # except Product.DoesNotExist:
    #     return None


# ERROR DE INTEGRACIÓN #3: Crear membresía con precio negativo
def create_membership_with_negative_price(user_id, plan_name, price):
    """
    Intenta crear una membresía con precio negativo (violación de lógica de negocio).
    
    Args:
        user_id: ID del usuario
        plan_name: Nombre del plan
        price: Precio (negativo)
    
    CASO DE USO PARA DEBUGGING:
    1. Establecer breakpoint en línea 146
    2. Llamar: create_membership_with_negative_price(1, 'PREMIUM', -99.90)
    3. Inspeccionar user_id, plan_name y price
    4. Ver que price es negativo
    5. El sistema permite crear pero viola regla de negocio
    """
    from apps.memberships.models import Membership
    from datetime import timedelta
    from django.utils import timezone
    
    print(f"[DEBUG] Creando membresía...")
    print(f"[DEBUG] User ID: {user_id}")
    print(f"[DEBUG] Plan: {plan_name}")
    print(f"[DEBUG] Precio: ${price}")
    
    user = User.objects.get(id=user_id)
    
    # BUG INTENCIONAL: no valida que el precio sea positivo
    membership = Membership.objects.create(
        user=user,
        plan_name=plan_name,
        price=Decimal(str(price)),  # ❌ Permite precio negativo
        start_date=timezone.now().date(),
        end_date=timezone.now().date() + timedelta(days=30),
        status='ACTIVE'
    )
    
    print(f"[DEBUG] Membresía creada: {membership.id}")
    return membership
    
    # CORRECCIÓN:
    # if price <= 0:
    #     raise ValueError("El precio debe ser positivo")


# ERROR DE INTEGRACIÓN #4: Circular dependency o FK constraint
def delete_user_with_payments(user_id):
    """
    Intenta eliminar usuario que tiene pagos asociados (violación de integridad referencial).
    
    Args:
        user_id: ID del usuario a eliminar
    
    CASO DE USO PARA DEBUGGING:
    1. Establecer breakpoint en línea 195
    2. Crear usuario con pagos primero
    3. Llamar: delete_user_with_payments(user_id)
    4. Inspeccionar user y sus relaciones
    5. Ver ProtectedError o CASCADE según configuración
    """
    print(f"[DEBUG] Eliminando usuario...")
    print(f"[DEBUG] User ID: {user_id}")
    
    user = User.objects.get(id=user_id)
    
    print(f"[DEBUG] Pagos del usuario: {user.payments.count()}")
    print(f"[DEBUG] Membresías del usuario: {user.memberships.count()}")
    
    # BUG INTENCIONAL: intenta eliminar sin verificar relaciones
    user.delete()  # ❌ Puede causar CASCADE no deseado o ProtectedError
    
    print(f"[DEBUG] Usuario eliminado")
    
    # CORRECCIÓN:
    # if user.payments.exists() or user.memberships.exists():
    #     raise ValueError("No se puede eliminar usuario con datos asociados")


if __name__ == "__main__":
    print("=" * 60)
    print("TESTING ERRORES DE INTEGRACIÓN")
    print("=" * 60)
    print("\n⚠️  ADVERTENCIA: Estos tests modifican la base de datos")
    print("=" * 60)
    
    # Test 1: Pago sin usuario
    print("\n1. Test de pago sin usuario:")
    try:
        payment = create_payment_without_user(100, 'CASH')
        print(f"✓ Pago creado: {payment.id}")
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
    
    # Test 2: Producto inexistente
    print("\n2. Test de producto inexistente:")
    try:
        movement = update_stock_for_nonexistent_product(99999, 10)
        print(f"✓ Movimiento creado: {movement.id}")
    except Product.DoesNotExist as e:
        print(f"❌ ERROR: Producto no existe")
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
    
    # Test 3: Precio negativo
    print("\n3. Test de membresía con precio negativo:")
    try:
        user = User.objects.first()
        if user:
            membership = create_membership_with_negative_price(user.id, 'PREMIUM', -99.90)
            print(f"⚠️  Membresía creada con precio negativo: {membership.id}")
            print(f"   Precio: ${membership.price} (violación de regla de negocio)")
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
    
    # Test 4: Eliminar usuario con relaciones
    print("\n4. Test de eliminar usuario con relaciones:")
    try:
        user = User.objects.filter(payments__isnull=False).first()
        if user:
            delete_user_with_payments(user.id)
            print(f"✓ Usuario eliminado")
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
