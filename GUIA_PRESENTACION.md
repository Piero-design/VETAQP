# 🎯 Guía de Presentación - Debugging VETAQP

## 📋 CHECKLIST PRE-PRESENTACIÓN (5 minutos antes)

```bash
# 1. Abrir VS Code en el proyecto
cd /Users/piero.o/Documents/GitHub/AQPVET/proyectoAQPVET_CS_FINAL

# 2. Tener listos 3 terminales:
# Terminal 1: Para ejecutar errores
# Terminal 2: Para Django (si es necesario)
# Terminal 3: Para git/comandos generales

# 3. Archivos a tener abiertos en pestañas:
# - INFORME_DEBUGGING.md (este es tu guion)
# - debugging_examples/logical_errors.py
# - debugging_examples/runtime_errors.py
# - debugging_examples/integration_errors.py
# - .vscode/launch.json

# 4. Cerrar pestañas innecesarias
# 5. Zoom al 125% para que se vea bien en proyector
# 6. Tema claro de VS Code (más visible en proyector)
```

---

## 🎬 ESTRUCTURA DE LA PRESENTACIÓN (15-20 minutos)

### **PARTE 1: Introducción al Proyecto** (2 minutos)

**Qué mostrar:**
1. Abrir el proyecto en VS Code
2. Mostrar estructura de carpetas en el explorador lateral

**Qué decir:**
> "Buenos días/tardes. Voy a presentar el trabajo de debugging del proyecto VETAQP, un sistema veterinario con Django + React. El proyecto tiene estos módulos implementados: usuarios, mascotas, productos, inventario, pagos y membresías."

**Mostrar en pantalla:**
```
proyectoAQPVET_CS_FINAL/
├── backend/
│   ├── apps/
│   │   ├── inventory/      ← Módulos reales con validaciones
│   │   ├── payments/
│   │   ├── memberships/
│   └── debugging_examples/  ← ⭐ Errores intencionales para práctica
│       ├── logical_errors.py
│       ├── runtime_errors.py
│       └── integration_errors.py
└── INFORME_DEBUGGING.md     ← Documentación completa
```

**Decir:**
> "Creamos una carpeta **`debugging_examples/`** con errores intencionales para cumplir con el requisito de debugging. Estos errores NO afectan el sistema real, que está en la carpeta `apps/` con todas sus validaciones correctas."

---

### **PARTE 2: Demostración de Errores** (8-10 minutos)

#### 🔴 **DEMO 1: Error Lógico - Descuento Incorrecto** (2 min)

**Archivo:** `logical_errors.py`

**Script:**
1. Abrir el archivo en VS Code
2. Mostrar la función problemática (línea 28):

**Qué decir:**
> "Primer ejemplo: error lógico en cálculo de descuento. Este tipo de error NO genera excepciones, pero produce resultados incorrectos."

**Código a mostrar:**
```python
def calculate_membership_discount(base_price, discount_percentage):
    # ❌ ERROR: Resta en lugar de calcular porcentaje
    discount_amount = base_price - discount_percentage  # Línea 28
    final_price = base_price - discount_amount
    return final_price
```

**Ejecutar en terminal:**
```bash
cd backend
python debugging_examples/logical_errors.py
```

**Mostrar output:**
```
=== ERROR LÓGICO 1: Cálculo de descuento ===
Precio base: $100
Descuento: 20%
Precio con descuento: $20.00  ← ❌ INCORRECTO (debería ser $80)
```

**Debugging en vivo con VS Code:**
1. Colocar breakpoint en línea 28 (click en margen izquierdo)
2. Presionar **F5** → "Python: Current File"
3. Cuando pause, mostrar panel **VARIABLES**:
   - `base_price = 100`
   - `discount_percentage = 20`
4. Presionar **F10** para ejecutar línea 28
5. Mostrar: `discount_amount = 80` (❌ debería ser 20)
6. Presionar **F10** otra vez
7. Mostrar: `final_price = 20` (❌ debería ser 80)

**Explicar la corrección:**
> "El error está aquí: resta directamente en lugar de calcular el porcentaje. La corrección sería:"
```python
discount_amount = base_price * (discount_percentage / 100)  # 100 * 0.20 = 20
final_price = base_price - discount_amount  # 100 - 20 = 80
```

---

#### 🔴 **DEMO 2: Error Runtime - División por Cero** (2 min)

**Archivo:** `runtime_errors.py`

**Qué decir:**
> "Segundo ejemplo: error de ejecución. Este SÍ genera una excepción que detiene el programa."

**Código a mostrar (línea 30):**
```python
def calculate_average_payment(total_amount, number_of_payments):
    # ❌ ERROR: No valida división por cero
    average = total_amount / number_of_payments
    return average
```

**Ejecutar:**
```bash
python debugging_examples/runtime_errors.py
```

**Mostrar el crash:**
```
=== ERROR DE EJECUCIÓN 1: División por cero ===
Traceback (most recent call last):
  File "debugging_examples/runtime_errors.py", line 36, in <module>
    result = calculate_average_payment(500.00, 0)
  File "debugging_examples/runtime_errors.py", line 30, in calculate_average_payment
    average = total_amount / number_of_payments
ZeroDivisionError: division by zero
```

**Explicar:**
> "Python lanza `ZeroDivisionError`. El stack trace nos dice exactamente dónde falló: línea 30. La corrección es validar antes de dividir:"

```python
if number_of_payments == 0:
    return 0
return total_amount / number_of_payments
```

---

#### 🔴 **DEMO 3: Error Integración - Django IntegrityError** (3 min)

**Archivo:** `integration_errors.py`

**Qué decir:**
> "Tercer ejemplo: error de integración con Django. Ocurre cuando hay problemas en la interacción entre componentes (base de datos, modelos)."

**Código a mostrar (línea 30-35):**
```python
def create_payment_without_user():
    # ❌ ERROR: Intenta crear pago sin usuario (campo requerido)
    payment = Payment.objects.create(
        user=None,  # ← Viola restricción NOT NULL
        amount=100.00,
        payment_method='CASH',
        status='PENDING'
    )
```

**Ejecutar:**
```bash
python debugging_examples/integration_errors.py
```

**Mostrar el error Django:**
```
=== ERROR DE INTEGRACIÓN 1: Payment sin usuario ===
django.db.utils.IntegrityError: NOT NULL constraint failed: apps_payment.user_id
```

**Explicar:**
> "Django lanza `IntegrityError` porque el campo `user` tiene una restricción NOT NULL en la base de datos. La corrección es siempre asignar un usuario válido:"

```python
user = User.objects.first()
if user is None:
    raise ValueError("No hay usuarios en el sistema")
payment = Payment.objects.create(user=user, amount=100.00, ...)
```

---

### **PARTE 3: Herramientas de Debugging** (3 minutos)

**Mostrar en pantalla:** `.vscode/launch.json`

**Qué decir:**
> "Configuramos VS Code con 5 configuraciones de debugging para diferentes escenarios."

**Mostrar el archivo:**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Django",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/backend/manage.py",
            "args": ["runserver", "--noreload"]
        },
        {
            "name": "Debug Logical Errors",
            "type": "debugpy",
            "program": "${workspaceFolder}/backend/debugging_examples/logical_errors.py"
        }
    ]
}
```

**Demostrar las 3 técnicas:**

#### 1. **pdb (Python Debugger)**
> "Primera herramienta: pdb desde línea de comandos."

Mostrar en `logical_errors.py`:
```python
import pdb
pdb.set_trace()  # ← Breakpoint manual
```

**Comandos a demostrar:**
```bash
python debugging_examples/logical_errors.py
(Pdb) n              # next: siguiente línea
(Pdb) p base_price   # print: ver variable
(Pdb) l              # list: ver código
(Pdb) c              # continue: continuar
```

#### 2. **Breakpoints en VS Code**
> "Segunda herramienta: breakpoints visuales en VS Code."

1. Click en margen izquierdo (punto rojo)
2. **F5** para iniciar
3. **F10** para siguiente línea
4. **F11** para entrar en función
5. Panel **VARIABLES** muestra todo automáticamente

**Mostrar breakpoint condicional:**
1. Click derecho en breakpoint
2. "Edit Breakpoint" → "Expression"
3. Escribir: `required_quantity > 10`
4. Solo pausa si se cumple la condición

#### 3. **print() debugging**
> "Tercera técnica: prints estratégicos para debugging rápido."

```python
print(f"DEBUG: user_data = {user_data}")
print(f"DEBUG: keys = {user_data.keys()}")
membership_info = user_data['memberships']  # ← Error aquí
```

---

### **PARTE 4: Resultados y Aprendizajes** (3 minutos)

**Abrir:** `INFORME_DEBUGGING.md`

**Scroll a la tabla de resumen:**

| Tipo de Error | Cantidad | Archivos |
|--------------|----------|----------|
| Errores Lógicos | 3 | `logical_errors.py` |
| Errores de Ejecución | 4 | `runtime_errors.py` |
| Errores de Integración | 4 | `integration_errors.py` |
| **TOTAL** | **11 errores** | (requisito: 6 mínimo) ✅ |

**Qué decir:**
> "Implementamos 11 errores intencionales, superando el requisito de 6. Documentamos 6 casos de uso con debugging paso a paso."

**Mostrar tabla de técnicas:**

| Técnica | Casos de Uso |
|---------|--------------|
| pdb | Casos 1 y 6 |
| VS Code Breakpoints | Casos 2, 3, 5 |
| print() | Caso 4 |

**Scroll a "¿Qué aprendimos?"**

Destacar 3 lecciones principales:

> "Los 3 aprendizajes más importantes fueron:
> 
> 1. **Los errores lógicos son los más difíciles** porque no generan excepciones
> 2. **El stack trace es tu mejor amigo** - siempre leerlo de abajo hacia arriba
> 3. **Validar siempre las entradas** antes de operar con ellas"

**Mostrar impacto en el proyecto:**

```
Antes del debugging:
❌ No validábamos casos límite
❌ Errores lógicos pasaban desapercibidos

Después del debugging:
✅ 15 tests de integración (todos pasando)
✅ Validaciones en todos los serializers
✅ 0 crashes en testing manual
```

---

### **PARTE 5: Sistema Real vs Ejemplos** (2 minutos)

**Mostrar archivo real:** `apps/payments/serializers/__init__.py`

**Qué decir:**
> "Importante aclarar: los errores de `debugging_examples/` son solo para práctica. El sistema real en `apps/` tiene todas las validaciones correctas."

**Mostrar código real:**
```python
class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method', 'transaction_id', 'notes']
    
    def validate_amount(self, value):
        if value <= 0:  # ✅ Validación correcta
            raise serializers.ValidationError("El monto debe ser mayor a cero.")
        return value
```

**Ejecutar tests para demostrar:**
```bash
python manage.py test apps.payments.tests_integration -v 2
```

**Mostrar output:**
```
test_create_payment ... ok
test_filter_payments_by_status ... ok
test_list_payments ... ok
test_list_payments_requires_auth ... ok
test_payment_detail ... ok

----------------------------------------------------------------------
Ran 5 tests in 1.234s

OK ✅
```

---

### **PARTE 6: Repositorio GitHub** (1 minuto)

**Abrir navegador:** https://github.com/Piero-design/VETAQP

**Qué decir:**
> "Todo el código está en GitHub, incluyendo los ejemplos de debugging y la documentación completa."

**Mostrar en GitHub:**
1. Carpeta `debugging_examples/`
2. Archivo `INFORME_DEBUGGING.md`
3. Commits recientes con mensajes descriptivos

---

## 🎤 RESPUESTAS A PREGUNTAS FRECUENTES

### P: "¿Estos errores están en el sistema real?"
**R:** "No, están en la carpeta `debugging_examples/` separada. El sistema real en `apps/` tiene todas las validaciones correctas y 15 tests pasando."

### P: "¿Cómo detectaron cada error?"
**R:** "Usamos tres métodos:
1. **Stack traces** para errores de ejecución (crash inmediato)
2. **Debugger paso a paso** para errores lógicos (sin crash)
3. **Tests de integración** para errores de interacción Django"

### P: "¿Por qué usaron pdb Y VS Code?"
**R:** "Porque cada herramienta tiene ventajas:
- **pdb**: No requiere IDE, funciona en servidores
- **VS Code**: Interfaz visual, más fácil para código complejo
- Aprendimos ambas para estar preparados en diferentes escenarios"

### P: "¿Cuánto tiempo tomó?"
**R:** "La implementación de los errores y debugging: ~4 horas. La documentación: ~2 horas. Total: ~6 horas de trabajo."

### P: "¿Qué fue lo más difícil?"
**R:** "Los errores lógicos, porque no generan excepciones. Tuve que analizar el resultado esperado vs obtenido con el debugger paso a paso."

---

## ⚡ TIPS PARA LA PRESENTACIÓN

### ✅ HACER:
1. **Hablar claro y pausado** - el profesor necesita tiempo para entender
2. **Mostrar código antes de ejecutar** - explica qué va a pasar
3. **Zoom al 125%** - que se vea bien en proyector
4. **Tener agua cerca** - hablar 15 minutos da sed
5. **Practicar los comandos** - no quieres equivocarte en vivo
6. **Tener backup plan** - si algo falla, tienes screenshots o el informe

### ❌ NO HACER:
1. **No leer el informe palabra por palabra** - usa tus propias palabras
2. **No ir muy rápido** - mejor quedarse corto que perder al profesor
3. **No asumir conocimiento previo** - explica términos técnicos
4. **No esconder errores** - si algo falla, explícalo (es debugging!)
5. **No superar los 20 minutos** - respeta el tiempo

---

## 📊 ORDEN DE PESTAÑAS EN VS CODE (preparar antes)

```
Tab 1: INFORME_DEBUGGING.md (tu guion principal)
Tab 2: GUIA_PRESENTACION.md (esta guía, por si te pierdes)
Tab 3: debugging_examples/logical_errors.py
Tab 4: debugging_examples/runtime_errors.py
Tab 5: debugging_examples/integration_errors.py
Tab 6: apps/payments/serializers/__init__.py (para comparar con código real)
Tab 7: .vscode/launch.json (configuraciones)
```

---

## 🎬 SCRIPT COMPLETO (copia y pega en tu presentación)

### Inicio (30 segundos):
> "Buenos días/tardes. Soy [tu nombre] y voy a presentar el trabajo de debugging del proyecto VETAQP. El proyecto es un sistema veterinario con Django en el backend y React en el frontend. Implementamos 6 módulos completos: usuarios, mascotas, productos, inventario, pagos y membresías."

### Mostrar errores (5 min):
> "Para cumplir con el requisito de debugging, creamos 11 errores intencionales en la carpeta `debugging_examples/`. Voy a demostrar 3 ejemplos: uno lógico, uno de ejecución y uno de integración."

[Ejecutar las 3 demos como se indicó arriba]

### Herramientas (3 min):
> "Usamos tres herramientas de debugging: pdb para línea de comandos, breakpoints visuales en VS Code, y prints estratégicos. Les voy a mostrar cada una."

[Demostrar las 3 técnicas]

### Resultados (2 min):
> "Como resultado, implementamos 11 errores documentados, 6 casos de uso con debugging paso a paso, y agregamos validaciones al sistema real para prevenir estos errores en producción."

### Cierre (30 segundos):
> "Todo el código está en GitHub con documentación completa. El sistema real tiene 15 tests de integración pasando. ¿Tienen alguna pregunta?"

---

## ⏱️ CRONOGRAMA DETALLADO

| Tiempo | Actividad | Duración |
|--------|-----------|----------|
| 0:00 - 0:30 | Introducción | 30 seg |
| 0:30 - 2:30 | Demo Error Lógico | 2 min |
| 2:30 - 4:30 | Demo Error Runtime | 2 min |
| 4:30 - 7:30 | Demo Error Integración | 3 min |
| 7:30 - 10:30 | Herramientas (pdb, VS Code, print) | 3 min |
| 10:30 - 13:30 | Resultados y aprendizajes | 3 min |
| 13:30 - 15:30 | Sistema real vs ejemplos | 2 min |
| 15:30 - 16:30 | GitHub y cierre | 1 min |
| 16:30 - 20:00 | Preguntas | 3-4 min |

**Total: 16-20 minutos**

---

## 🚨 PLAN B - Si algo falla

### Si no funciona VS Code debugger:
> "Voy a usar pdb en su lugar, que funciona directamente en terminal"

### Si hay error de módulos:
```bash
cd backend
source ../venv/bin/activate  # Activar entorno virtual
python debugging_examples/logical_errors.py
```

### Si no arranca Django:
> "Voy a mostrar solo los errores en scripts Python, que no requieren Django"

### Si se corta internet:
> "Tengo todo en local, así que puedo continuar sin problemas. El repositorio GitHub lo pueden revisar después"

---

## 📸 SCREENSHOTS DE BACKUP

**Captura estos antes de presentar (por si algo falla):**
1. VS Code con breakpoint activo y panel VARIABLES
2. Terminal con output de error (ZeroDivisionError)
3. Django IntegrityError completo
4. Tests pasando (OK ✅)
5. Repositorio GitHub

---

## ✅ CHECKLIST FINAL

Antes de comenzar la presentación:
- [ ] VS Code abierto en el proyecto
- [ ] 3 terminales preparadas
- [ ] Archivos abiertos en pestañas ordenadas
- [ ] Zoom al 125%
- [ ] Tema claro de VS Code
- [ ] Entorno virtual activado
- [ ] Navegador con GitHub abierto
- [ ] Agua cerca
- [ ] Reloj visible para controlar tiempo
- [ ] Esta guía abierta en segunda pantalla (o impresa)

---

## 🎯 MENSAJE CLAVE PARA EL PROFESOR

> "Este trabajo demuestra que entendemos:
> 1. Los 3 tipos de errores (lógicos, ejecución, integración)
> 2. Cómo usar herramientas de debugging (pdb, VS Code, print)
> 3. Cómo detectar y corregir errores paso a paso
> 4. La importancia de validaciones y tests
> 5. Todo está documentado y en GitHub para revisión"

---

**¡Mucha suerte! 🍀**
