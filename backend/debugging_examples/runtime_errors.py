"""
ERRORES DE EJECUCIÓN (RUNTIME) INTENCIONALES
Estos errores causan excepciones durante la ejecución.
"""

# ERROR DE EJECUCIÓN #1: División por cero
# BUG: No valida que el divisor sea cero
def calculate_average_payment(total_amount, number_of_payments):
    """
    Calcula el promedio de pagos.
    
    Args:
        total_amount: Monto total
        number_of_payments: Número de pagos
    
    Returns:
        Promedio por pago
    
    CASO DE USO PARA DEBUGGING:
    1. Establecer breakpoint en línea 30
    2. Llamar: calculate_average_payment(1000, 0)
    3. Inspeccionar total_amount y number_of_payments
    4. Avanzar con F10 y ver la excepción ZeroDivisionError
    5. Observar el traceback y el valor de las variables
    """
    print(f"[DEBUG] Calculando promedio de pagos...")
    print(f"[DEBUG] Monto total: ${total_amount}")
    print(f"[DEBUG] Número de pagos: {number_of_payments}")
    
    # BUG INTENCIONAL: no valida división por cero
    average = total_amount / number_of_payments  # ❌ ZeroDivisionError si number_of_payments == 0
    
    print(f"[DEBUG] Promedio: ${average}")
    return average
    
    # CORRECCIÓN:
    # if number_of_payments == 0:
    #     return 0
    # average = total_amount / number_of_payments


# ERROR DE EJECUCIÓN #2: Acceso a clave inexistente en diccionario
# BUG: No verifica si la clave existe antes de acceder
def get_user_membership_info(user_data, membership_id):
    """
    Obtiene información de membresía de un usuario.
    
    Args:
        user_data: Diccionario con datos del usuario
        membership_id: ID de la membresía
    
    Returns:
        Información de la membresía
    
    CASO DE USO PARA DEBUGGING:
    1. Establecer breakpoint en línea 66
    2. Llamar: get_user_membership_info({'name': 'Juan', 'email': 'juan@test.com'}, 1)
    3. Inspeccionar user_data con el debugger
    4. Ver que 'memberships' no existe en el diccionario
    5. Avanzar y observar KeyError
    """
    print(f"[DEBUG] Obteniendo info de membresía...")
    print(f"[DEBUG] User data: {user_data}")
    print(f"[DEBUG] Membership ID: {membership_id}")
    
    # BUG INTENCIONAL: accede a clave sin verificar existencia
    memberships = user_data['memberships']  # ❌ KeyError si 'memberships' no existe
    
    membership = memberships.get(membership_id, None)
    print(f"[DEBUG] Membership: {membership}")
    
    return membership
    
    # CORRECCIÓN:
    # memberships = user_data.get('memberships', {})
    # o usar try-except


# ERROR DE EJECUCIÓN #3: Conversión de tipo inválida
def process_payment_amount(amount_str):
    """
    Procesa el monto de un pago desde string.
    
    Args:
        amount_str: Monto como string
    
    Returns:
        Monto como float
    
    CASO DE USO PARA DEBUGGING:
    1. Establecer breakpoint en línea 106
    2. Llamar: process_payment_amount("cien soles")
    3. Inspeccionar amount_str
    4. Avanzar y ver ValueError cuando intenta convertir
    """
    print(f"[DEBUG] Procesando monto de pago...")
    print(f"[DEBUG] Monto string: '{amount_str}'")
    
    # BUG INTENCIONAL: no valida antes de convertir
    amount = float(amount_str)  # ❌ ValueError si amount_str no es numérico
    
    print(f"[DEBUG] Monto convertido: ${amount}")
    return amount
    
    # CORRECCIÓN:
    # try:
    #     amount = float(amount_str)
    # except ValueError:
    #     return 0.0


# ERROR DE EJECUCIÓN #4: Índice fuera de rango
def get_first_active_membership(memberships_list):
    """
    Obtiene la primera membresía activa de una lista.
    
    Args:
        memberships_list: Lista de membresías
    
    Returns:
        Primera membresía activa
    
    CASO DE USO PARA DEBUGGING:
    1. Establecer breakpoint en línea 145
    2. Llamar: get_first_active_membership([])
    3. Inspeccionar memberships_list (está vacía)
    4. Avanzar y ver IndexError al intentar acceder al índice 0
    """
    print(f"[DEBUG] Buscando primera membresía activa...")
    print(f"[DEBUG] Lista de membresías: {memberships_list}")
    print(f"[DEBUG] Tamaño de lista: {len(memberships_list)}")
    
    # BUG INTENCIONAL: no valida que la lista tenga elementos
    first_membership = memberships_list[0]  # ❌ IndexError si lista vacía
    
    print(f"[DEBUG] Primera membresía: {first_membership}")
    return first_membership
    
    # CORRECCIÓN:
    # if not memberships_list:
    #     return None
    # first_membership = memberships_list[0]


if __name__ == "__main__":
    print("=" * 60)
    print("TESTING ERRORES DE EJECUCIÓN")
    print("=" * 60)
    
    # Test 1: División por cero
    print("\n1. Test de división por cero:")
    try:
        result = calculate_average_payment(1000, 0)
        print(f"Resultado: ${result}")
    except ZeroDivisionError as e:
        print(f"❌ ERROR: {e}")
    
    # Test 2: KeyError
    print("\n2. Test de acceso a clave inexistente:")
    try:
        user = {'name': 'Juan', 'email': 'juan@test.com'}
        info = get_user_membership_info(user, 1)
        print(f"Resultado: {info}")
    except KeyError as e:
        print(f"❌ ERROR: Clave no encontrada: {e}")
    
    # Test 3: ValueError
    print("\n3. Test de conversión inválida:")
    try:
        amount = process_payment_amount("cien soles")
        print(f"Resultado: ${amount}")
    except ValueError as e:
        print(f"❌ ERROR: {e}")
    
    # Test 4: IndexError
    print("\n4. Test de índice fuera de rango:")
    try:
        membership = get_first_active_membership([])
        print(f"Resultado: {membership}")
    except IndexError as e:
        print(f"❌ ERROR: {e}")
