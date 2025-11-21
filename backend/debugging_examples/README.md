# Debugging Examples - Errores Intencionales para Práctica

Este directorio contiene errores intencionales creados con propósitos educativos para practicar debugging con:
- pdb (Python Debugger)
- Breakpoints en VS Code
- print() controlado

## Errores Implementados:

### Errores Lógicos (2)
1. **Cálculo incorrecto de descuento en membresías** (logical_errors.py)
2. **Validación errónea de stock en inventory** (logical_errors.py)

### Errores de Ejecución (2)
1. **División por cero en cálculo de promedios** (runtime_errors.py)
2. **Acceso a clave inexistente en diccionario** (runtime_errors.py)

### Errores de Integración (2)
1. **Creación de pago sin usuario autenticado** (integration_errors.py)
2. **Actualización de stock con producto inexistente** (integration_errors.py)

## Cómo usar:

### Con pdb:
```python
import pdb
pdb.set_trace()  # Breakpoint
```

### Con VS Code:
1. Coloca un breakpoint (click en el margen izquierdo)
2. F5 para iniciar debugging
3. F10 para siguiente línea
4. F11 para entrar en función

### Con print():
```python
print(f"DEBUG: variable = {variable}")
```

## Comandos de pdb:
- `n` (next): Siguiente línea
- `s` (step): Entrar en función
- `c` (continue): Continuar ejecución
- `p variable`: Imprimir variable
- `l` (list): Ver código alrededor
- `q` (quit): Salir
