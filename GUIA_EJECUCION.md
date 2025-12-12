# Guía de Ejecución y Testing - Ecommerce VETAQP

## 🚀 Cómo Ejecutar el Proyecto

### Requisitos Previos
- Python 3.8+
- Node.js 14+
- npm o yarn
- Git

---

## 📦 Backend (Django)

### 1. Preparar el Entorno

```bash
# Navegar a la carpeta del backend
cd e:\UNSA2025B\Construccion Software\VETAQP\backend

# Crear entorno virtual (si no existe)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Base de Datos

```bash
# Aplicar migraciones
python manage.py migrate

# Crear superusuario (admin)
python manage.py createsuperuser
# Ingresar:
# Username: admin
# Email: admin@example.com
# Password: admin123

# Cargar datos de ejemplo (opcional)
python manage.py loaddata setup_demo_data.py
# O ejecutar:
python load_sample_data.py
```

### 3. Ejecutar el Servidor

```bash
# Iniciar servidor Django
python manage.py runserver 0.0.0.0:8000

# El servidor estará disponible en:
# http://localhost:8000
# Admin panel: http://localhost:8000/admin
```

---

## 🎨 Frontend (React)

### 1. Preparar el Entorno

```bash
# Navegar a la carpeta del frontend
cd e:\UNSA2025B\Construccion Software\VETAQP\frontend

# Instalar dependencias
npm install

# O con yarn:
yarn install
```

### 2. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del frontend:

```env
VITE_API_URL=http://localhost:8000/api
```

### 3. Ejecutar el Servidor de Desarrollo

```bash
# Iniciar servidor Vite
npm run dev

# O con yarn:
yarn dev

# El servidor estará disponible en:
# http://localhost:5173
```

---

## 🧪 Testing del Flujo de Compra

### Paso 1: Crear Cuenta

1. Ir a http://localhost:5173/register
2. Ingresar datos:
   - Usuario: `testuser`
   - Email: `test@example.com`
   - Contraseña: `test1234`
   - Confirmar: `test1234`
3. Hacer clic en "Registrarse"
4. Debería redirigir a login

### Paso 2: Iniciar Sesión

1. Ir a http://localhost:5173/login
2. Ingresar credenciales:
   - Usuario: `testuser`
   - Contraseña: `test1234`
3. Hacer clic en "Ingresar"
4. Debería redirigir a perfil y mostrar "👋 Hola, testuser" en navbar

### Paso 3: Navegar Catálogo

1. Hacer clic en "Inicio" o logo
2. Ver catálogo de productos
3. Probar filtros:
   - Filtro por tipo de mascota (Perros/Gatos)
   - Búsqueda por nombre
4. Debería mostrar productos filtrados

### Paso 4: Agregar al Carrito

1. Hacer clic en "Agregar" en cualquier producto
2. Ver notificación de éxito
3. Ver badge con cantidad en carrito (navbar)
4. Agregar 2-3 productos más

### Paso 5: Revisar Carrito

1. Hacer clic en icono de carrito (navbar)
2. Ver todos los productos agregados
3. Probar funciones:
   - Aumentar cantidad (+)
   - Disminuir cantidad (−)
   - Eliminar producto (✕)
   - Ver total actualizado
4. Hacer clic en "Proceder al pago"

### Paso 6: Checkout - Datos de Envío

1. Completar formulario:
   - Nombre: Juan Pérez
   - Email: juan@example.com
   - Teléfono: +51 999 999 999
   - Dirección: Calle Principal 123, Apto 4B
   - Ciudad: Arequipa
2. Hacer clic en "Continuar al pago"

### Paso 7: Checkout - Pago

1. Ver resumen de compra
2. Ver datos de pago simulado:
   - Tarjeta: 4532 1234 5678 9010
   - Vencimiento: 12/25
   - CVV: 123
3. Hacer clic en "Confirmar pago"
4. Debería crear la orden

### Paso 8: Confirmación de Pedido

1. Ver página de confirmación con:
   - Número de pedido (ej: ORD-ABC12345)
   - Estado: Pendiente
   - Total: S/ XXX.XX
   - Datos de envío
   - Productos comprados
2. Hacer clic en "Ver mis pedidos"

### Paso 9: Gestión de Pedidos

1. Ver lista de pedidos
2. Ver detalles del pedido creado
3. Probar filtro por estado
4. Hacer clic en "Ir al catálogo" para volver a comprar

### Paso 10: Seguimiento

1. Ir a "Servicios" → "Seguimiento"
2. Ver el pedido creado
3. Debería mostrar estado y detalles

---

## 🔐 Testing de Autenticación

### Test 1: Acceso sin Autenticación

```bash
# Intentar acceder a checkout sin token
curl -X GET http://localhost:8000/api/orders/

# Debería retornar 401 Unauthorized
```

### Test 2: Registro Duplicado

1. Intentar registrar usuario con mismo username
2. Debería mostrar error: "Este nombre de usuario ya existe"

### Test 3: Credenciales Inválidas

1. Ir a login
2. Ingresar usuario incorrecto
3. Debería mostrar: "Credenciales inválidas"

### Test 4: Token Expirado

1. Obtener token
2. Esperar a que expire (configurado en settings)
3. Intentar hacer request
4. Debería retornar 401 y permitir refresh

---

## 📊 Testing de Productos

### Test 1: Filtro por Tipo de Mascota

```bash
# Obtener productos para perros
curl -X GET "http://localhost:8000/api/products/?pet_type=dog"

# Debería retornar solo productos para perros
```

### Test 2: Búsqueda

```bash
# Buscar por nombre
curl -X GET "http://localhost:8000/api/products/?search=alimento"

# Debería retornar productos que contengan "alimento"
```

### Test 3: Ordenamiento

```bash
# Ordenar por precio (ascendente)
curl -X GET "http://localhost:8000/api/products/?ordering=price"

# Ordenar por precio (descendente)
curl -X GET "http://localhost:8000/api/products/?ordering=-price"

# Ordenar por fecha (más recientes)
curl -X GET "http://localhost:8000/api/products/?ordering=-created_at"
```

---

## 📋 Testing de Órdenes

### Test 1: Crear Orden

```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"product_id": 1, "quantity": 2},
      {"product_id": 2, "quantity": 1}
    ],
    "shipping_name": "Juan Pérez",
    "shipping_email": "juan@example.com",
    "shipping_phone": "+51 999 999 999",
    "shipping_address": "Calle Principal 123",
    "shipping_city": "Arequipa"
  }'
```

### Test 2: Listar Órdenes del Usuario

```bash
curl -X GET http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Debería retornar solo órdenes del usuario autenticado
```

### Test 3: Obtener Detalle de Orden

```bash
curl -X GET http://localhost:8000/api/orders/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Debería retornar detalles de la orden
```

### Test 4: Confirmar Pago

```bash
curl -X POST http://localhost:8000/api/orders/1/confirm_payment/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Debería cambiar payment_status a "completed"
```

---

## 🐛 Troubleshooting

### Problema: CORS Error

**Síntoma**: Error en consola: "Access to XMLHttpRequest blocked by CORS policy"

**Solución**:
```python
# En backend/aqpvet/settings.py, agregar:
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
]
```

### Problema: Token No Válido

**Síntoma**: Error 401 en requests autenticados

**Solución**:
1. Verificar que el token se está guardando en localStorage
2. Verificar que el token no ha expirado
3. Hacer refresh del token si es necesario

### Problema: Productos No Aparecen

**Síntoma**: Catálogo vacío

**Solución**:
1. Verificar que hay productos en la base de datos
2. Verificar que los productos tienen status='active'
3. Ejecutar: `python load_sample_data.py`

### Problema: Carrito No Persiste

**Síntoma**: Carrito se vacía al recargar

**Solución**:
1. Verificar que localStorage está habilitado
2. Verificar en DevTools → Application → Local Storage
3. Limpiar localStorage y volver a intentar

### Problema: Email No Se Envía

**Síntoma**: No llegan emails de confirmación

**Solución**:
1. Configurar SMTP en settings.py
2. Usar servicio como SendGrid, Mailgun, etc.
3. Para desarrollo, usar console backend:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

---

## 📈 Monitoreo y Logs

### Ver Logs del Backend

```bash
# Los logs aparecen en la consola donde ejecutaste runserver
# Para más detalle, agregar en settings.py:

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

### Ver Logs del Frontend

```bash
# Abrir DevTools (F12)
# Console → Ver todos los logs
# Network → Ver requests/responses
# Application → Local Storage, Cookies
```

---

## 🧪 Casos de Prueba Automatizados

### Test de Registro

```javascript
// frontend/src/__tests__/Register.test.jsx
test('Registrar usuario exitosamente', async () => {
  render(<Register />);
  
  fireEvent.change(screen.getByLabelText(/usuario/i), {
    target: { value: 'testuser' }
  });
  fireEvent.change(screen.getByLabelText(/correo/i), {
    target: { value: 'test@example.com' }
  });
  fireEvent.change(screen.getByLabelText(/contraseña/i), {
    target: { value: 'test1234' }
  });
  
  fireEvent.click(screen.getByRole('button', { name: /registrarse/i }));
  
  await waitFor(() => {
    expect(screen.getByText(/cuenta creada/i)).toBeInTheDocument();
  });
});
```

### Test de Carrito

```javascript
// frontend/src/__tests__/Cart.test.jsx
test('Agregar producto al carrito', () => {
  const { addToCart } = useCart();
  
  const product = { id: 1, name: 'Alimento', price: 50 };
  addToCart(product);
  
  expect(cart).toContainEqual({
    ...product,
    quantity: 1
  });
});
```

---

## 📱 Testing en Dispositivos Móviles

### Desde la Misma Red

```bash
# Obtener IP local
ipconfig getifaddr en0  # Mac
ipconfig              # Windows

# Acceder desde móvil
http://192.168.1.100:5173
```

### Usando DevTools

```bash
# En Chrome DevTools
# Toggle device toolbar (Ctrl+Shift+M)
# Probar diferentes tamaños de pantalla
```

---

## 🚀 Deployment

### Preparar para Producción

```bash
# Backend
python manage.py collectstatic
python manage.py check --deploy

# Frontend
npm run build
# Esto crea carpeta dist/ lista para servir
```

### Opciones de Hosting

**Backend**:
- Heroku
- PythonAnywhere
- AWS EC2
- DigitalOcean
- Railway

**Frontend**:
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

---

## 📞 Soporte

Si encuentras problemas:
1. Revisar logs del backend y frontend
2. Verificar que ambos servidores están corriendo
3. Limpiar cache del navegador (Ctrl+Shift+Delete)
4. Reiniciar ambos servidores
5. Verificar que las URLs son correctas

