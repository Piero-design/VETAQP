"""
ERRORES LÓGICOS INTENCIONALES
Estos errores no causan excepciones pero producen resultados incorrectos.
"""

# ERROR LÓGICO #1: Cálculo incorrecto de descuento en membresías
# BUG: El descuento se resta en lugar de multiplicar por el complemento
def calculate_membership_discount(base_price, discount_percentage):
    """
    Calcula el precio con descuento de una membresía.
    
    Args:
        base_price: Precio base de la membresía
        discount_percentage: Porcentaje de descuento (ej: 20 para 20%)
    
    Returns:
        Precio final con descuento aplicado
    
    CASO DE USO PARA DEBUGGING:
    1. Establecer breakpoint en línea 28
    2. Llamar: calculate_membership_discount(100, 20)
    3. Inspeccionar variables base_price, discount_percentage, discount_amount
    4. Avanzar paso a paso y ver que el resultado es -20 en lugar de 80
    5. El error: debería ser base_price * (1 - discount_percentage/100)
    """
    print(f"[DEBUG] Calculando descuento...")
    print(f"[DEBUG] Precio base: {base_price}")
    print(f"[DEBUG] Descuento %: {discount_percentage}")
    
    # BUG INTENCIONAL: resta el porcentaje directamente
    discount_amount = base_price - discount_percentage  # ❌ INCORRECTO
    
    print(f"[DEBUG] Precio final: {discount_amount}")
    return discount_amount
    
    # CORRECCIÓN:
    # discount_amount = base_price * (1 - discount_percentage / 100)


# ERROR LÓGICO #2: Validación errónea de stock disponible
# BUG: La comparación usa >= en lugar de >
def check_stock_availability(current_stock, requested_quantity):
    """
    Verifica si hay suficiente stock para una orden.
    
    Args:
        current_stock: Cantidad actual en inventario
        requested_quantity: Cantidad solicitada
    
    Returns:
        True si hay stock suficiente, False en caso contrario
    
    CASO DE USO PARA DEBUGGING:
    1. Establecer breakpoint en línea 62
    2. Llamar: check_stock_availability(10, 10)
    3. Inspeccionar current_stock y requested_quantity
    4. Ver que retorna False cuando debería retornar True
    5. El error: >= debería ser >, o invertir la condición
    """
    print(f"[DEBUG] Verificando stock...")
    print(f"[DEBUG] Stock actual: {current_stock}")
    print(f"[DEBUG] Cantidad solicitada: {requested_quantity}")
    
    # BUG INTENCIONAL: usa >= cuando debería ser <
    if current_stock >= requested_quantity:  # ❌ LÓGICA INVERTIDA
        print(f"[DEBUG] Stock insuficiente")
        return False
    
    print(f"[DEBUG] Stock suficiente")
    return True
    
    # CORRECCIÓN:
    # if current_stock < requested_quantity:
    #     return False
    # return True


# ERROR LÓGICO #3: Cálculo incorrecto de días restantes
def calculate_days_remaining(end_date_str):
    """
    Calcula los días restantes de una membresía.
    
    Args:
        end_date_str: Fecha de fin en formato 'YYYY-MM-DD'
    
    Returns:
        Número de días restantes
    
    CASO DE USO PARA DEBUGGING:
    1. Establecer breakpoint en línea 100
    2. Llamar con fecha futura: calculate_days_remaining('2025-12-31')
    3. Inspeccionar end_date, today, delta
    4. Ver que usa .days en lugar de considerar la diferencia completa
    """
    from datetime import datetime
    
    print(f"[DEBUG] Calculando días restantes...")
    print(f"[DEBUG] Fecha fin: {end_date_str}")
    
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    today = datetime.now()
    
    # BUG INTENCIONAL: invierte el orden de la resta
    delta = today - end_date  # ❌ INCORRECTO (debería ser end_date - today)
    
    days = delta.days
    print(f"[DEBUG] Días restantes: {days}")
    
    return days if days > 0 else 0
    
    # CORRECCIÓN:
    # delta = end_date - today


if __name__ == "__main__":
    print("=" * 60)
    print("TESTING ERRORES LÓGICOS")
    print("=" * 60)
    
    # Test 1: Descuento incorrecto
    print("\n1. Test de descuento:")
    result = calculate_membership_discount(100, 20)
    print(f"Resultado: ${result} (Esperado: $80, Obtenido: ${result})")
    
    # Test 2: Stock availability
    print("\n2. Test de stock:")
    available = check_stock_availability(10, 10)
    print(f"Resultado: {available} (Esperado: True, Obtenido: {available})")
    
    # Test 3: Días restantes
    print("\n3. Test de días restantes:")
    days = calculate_days_remaining('2025-12-31')
    print(f"Resultado: {days} días (Esperado: positivo, Obtenido: {days})")
