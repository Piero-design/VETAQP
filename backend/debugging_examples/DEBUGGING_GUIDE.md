# Guía de Debugging en VS Code para el Proyecto VETAQP

## Configuración de VS Code para Debugging Python/Django

### 1. Instalar extensión Python
- Instalar "Python" de Microsoft desde Extensions (Ctrl+Shift+X)

### 2. Crear configuración de debugging

Crear archivo `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Django",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/backend/manage.py",
            "args": [
                "runserver",
                "--noreload"
            ],
            "django": true,
            "justMyCode": false
        },
        {
            "name": "Python: Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": false
        }
    ]
}
```

## 6 Casos de Uso de Debugging

### CASO 1: Error Lógico - Descuento Incorrecto
**Archivo:** `debugging_examples/logical_errors.py`

**Pasos:**
1. Abrir `logical_errors.py`
2. Colocar **breakpoint** en línea 28 (click en margen izquierdo)
3. Presionar **F5** y seleccionar "Python: Current File"
4. Presionar **F10** para avanzar línea por línea
5. En el panel **VARIABLES** inspeccionar:
   - `base_price` = 100
   - `discount_percentage` = 20
   - `discount_amount` = 80 (INCORRECTO, debería ser 80)
6. Ver que el cálculo resta en lugar de aplicar porcentaje
7. Presionar **F5** para continuar

**Error identificado:** Línea 28 hace `base_price - discount_percentage` en lugar de `base_price * (1 - discount_percentage/100)`

---

### CASO 2: Error de Ejecución - División por Cero
**Archivo:** `debugging_examples/runtime_errors.py`

**Pasos:**
1. Abrir `runtime_errors.py`
2. Colocar **breakpoint** en línea 30
3. Presionar **F5**
4. En la **consola integrada** ver las variables de debug
5. Inspeccionar `number_of_payments` = 0
6. Presionar **F10** hasta llegar a la división
7. Ver **ZeroDivisionError** en el panel CALL STACK
8. Verificar el traceback

**Error identificado:** No se valida que `number_of_payments` sea diferente de cero antes de dividir

---

### CASO 3: Error de Integración - Producto Inexistente
**Archivo:** `debugging_examples/integration_errors.py`

**Pasos:**
1. Abrir `integration_errors.py`
2. Colocar **breakpoint** en línea 95
3. **Breakpoint condicional:** Click derecho en breakpoint → "Edit Breakpoint" → `product_id > 1000`
4. Presionar **F5**
5. Inspeccionar **CALL STACK** cuando se detiene
6. En **WATCH** agregar expresión: `Product.objects.filter(id=product_id).exists()`
7. Ver que retorna `False`
8. Presionar **F10** hasta `Product.objects.get()` y ver la excepción

**Error identificado:** No se valida existencia del producto antes de hacer `.get()`

---

### CASO 4: Error Lógico - Stock Availability
**Archivo:** `debugging_examples/logical_errors.py`

**Pasos:**
1. Abrir `logical_errors.py`
2. Colocar **breakpoint** en línea 62
3. Presionar **F5**
4. Con **F11** (Step Into) entrar en la función
5. En **DEBUG CONSOLE** ejecutar:
   ```python
   current_stock
   requested_quantity
   current_stock >= requested_quantity
   ```
6. Ver que la condición es True pero retorna False
7. Identificar lógica invertida

**Error identificado:** La condición `>=` está al revés, debería retornar `True` cuando hay suficiente stock

---

### CASO 5: Error de Ejecución - KeyError
**Archivo:** `runtime_errors.py`

**Pasos:**
1. Abrir `runtime_errors.py`
2. Colocar **breakpoint** en línea 66
3. Presionar **F5**
4. En panel **VARIABLES** expandir `user_data`
5. Ver las claves disponibles: `name`, `email` (NO hay `memberships`)
6. Presionar **F10** y ver **KeyError**
7. En **DEBUG CONSOLE** probar:
   ```python
   'memberships' in user_data  # False
   user_data.get('memberships', {})  # Solución
   ```

**Error identificado:** Acceso directo a clave sin verificar existencia

---

### CASO 6: Error de Integración - Pago sin Usuario
**Archivo:** `integration_errors.py`

**Pasos:**
1. Abrir `integration_errors.py`
2. Colocar **breakpoint** en línea 52
3. Configurar **Django debugging** en VS Code
4. Presionar **F5** con configuración "Python: Django"
5. Inspeccionar objeto `payment` en **VARIABLES**
6. Ver que `user` no está asignado (None o ausente)
7. Presionar **F10** hasta `payment.save()`
8. Ver **IntegrityError** en el panel **PROBLEMS**

**Error identificado:** Campo requerido `user` no está asignado antes de guardar

---

## Comandos de Debugging en VS Code

| Tecla | Acción |
|-------|--------|
| **F5** | Iniciar/Continuar debugging |
| **F9** | Toggle breakpoint |
| **F10** | Step Over (siguiente línea) |
| **F11** | Step Into (entrar en función) |
| **Shift+F11** | Step Out (salir de función) |
| **Ctrl+Shift+F5** | Restart debugging |
| **Shift+F5** | Stop debugging |

## Paneles Importantes

1. **VARIABLES:** Ver todas las variables locales y globales
2. **WATCH:** Agregar expresiones personalizadas para monitorear
3. **CALL STACK:** Ver la pila de llamadas de funciones
4. **BREAKPOINTS:** Gestionar todos los breakpoints
5. **DEBUG CONSOLE:** Ejecutar código Python en el contexto actual

## Tipos de Breakpoints

### Breakpoint Simple
- Click en margen izquierdo

### Breakpoint Condicional
- Click derecho → "Add Conditional Breakpoint"
- Ejemplo: `x > 10` (solo se detiene si x es mayor a 10)

### Logpoint
- Click derecho → "Add Logpoint"
- Imprime mensaje sin detener ejecución
- Ejemplo: `"Valor de x: {x}"`

## Debugging con pdb

Para usar pdb en lugar de VS Code:

```python
import pdb

def mi_funcion():
    x = 10
    pdb.set_trace()  # Breakpoint
    y = x * 2
    return y
```

**Comandos pdb:**
- `n` (next): Siguiente línea
- `s` (step): Entrar en función
- `c` (continue): Continuar hasta próximo breakpoint
- `p variable`: Imprimir variable
- `pp variable`: Pretty print
- `l` (list): Mostrar código
- `w` (where): Stack trace
- `q` (quit): Salir

## Uso de print() Controlado

```python
DEBUG = True

def debug_print(*args, **kwargs):
    if DEBUG:
        print("[DEBUG]", *args, **kwargs)

# Uso
debug_print(f"Variable x = {x}")
```

## Recomendaciones

1. **Siempre inspeccionar variables** antes del error
2. **Usar Call Stack** para entender el flujo
3. **Breakpoints condicionales** para loops grandes
4. **Debug Console** para probar soluciones en tiempo real
5. **Watch expressions** para monitorear valores específicos
6. **Logpoints** para no interrumpir la ejecución continuamente
