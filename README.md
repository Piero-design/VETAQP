# 🚀 AQPVET - Guía de Inicio Rápido

## 📋 Requisitos Previos

- Python 3.13+
- Node.js 18+
- npm 9+
- Git

---

## ⚡ Inicio Rápido (5 minutos)

### 1️⃣ Clonar el Repositorio
```bash
git clone https://github.com/Piero-design/VETAQP.git
cd VETAQP/proyectoAQPVET_CS_FINAL
```

### 2️⃣ Configurar Backend

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# Instalar dependencias
cd backend
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Crear superusuario (staff)
python manage.py createsuperuser
# Username: admin
# Email: admin@aqpvet.com
# Password: admin123

# Iniciar servidor Django
python manage.py runserver
```

El backend estará disponible en: **http://localhost:8000**

### 3️⃣ Configurar Frontend

Abrir una nueva terminal:

```bash
cd proyectoAQPVET_CS_FINAL/frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

El frontend estará disponible en: **http://localhost:5173**

---

## 🧪 Ejecutar Tests

### Backend - Todos los módulos
```bash
cd backend
source ../venv/bin/activate

# Tests de Chat (18 tests)
python manage.py test apps.chat.tests_integration -v 2

# Tests de Historial Médico (26 tests)
python manage.py test apps.pets.tests_integration -v 2

# Tests de Delivery (18 tests)
python manage.py test apps.orders.tests_integration -v 2

# Tests de Dashboard (12 tests)
python manage.py test apps.dashboard.tests_integration -v 2

# Todos los tests
python manage.py test -v 2
```

---

## 👥 Usuarios de Prueba

### Usuario Administrador (Staff)
- **Username:** admin
- **Password:** admin123
- **Permisos:** Acceso completo a dashboard, gestión de usuarios, productos, etc.

### Usuario Regular (crear desde /register)
- **Permisos:** Puede hacer pedidos, reservar citas, chat, gestionar mascotas

---

## 🎯 Funcionalidades Principales

### Para Usuarios Regulares
1. **Catálogo de Productos** - http://localhost:5173/
   - Buscar y filtrar productos
   - Añadir al carrito
   - Realizar compras

2. **Mis Mascotas** - http://localhost:5173/pets
   - Registrar mascotas
   - Ver información detallada

3. **Historial Médico** - http://localhost:5173/medical-history
   - Ver historial de cada mascota
   - Consultar vacunas aplicadas
   - Ver registros médicos

4. **Reservar Citas** - http://localhost:5173/appointments
   - Agendar citas veterinarias
   - Seleccionar fecha, hora y mascota
   - Ver estado de citas

5. **Chat con Veterinario** - http://localhost:5173/chat
   - Conversaciones en tiempo real
   - Historial de mensajes

6. **Mis Pedidos** - http://localhost:5173/orders
   - Ver historial de compras
   - Estado de pedidos

7. **Seguimiento de Envíos** - http://localhost:5173/order-tracking
   - Rastrear pedidos en tránsito
   - Ver timeline de estados
   - Tracking number

8. **Notificaciones** - http://localhost:5173/notifications
   - Centro de notificaciones
   - Alertas importantes

### Para Administradores (Staff)
Todas las anteriores más:

9. **Dashboard** - http://localhost:5173/dashboard 📊
   - **Estadísticas generales:** Pedidos, ingresos, usuarios, citas
   - **Ventas en el tiempo:** Análisis diario/semanal/mensual
   - **Productos populares:** Top 5 más vendidos
   - **Alertas de stock:** Productos con inventario bajo
   - **Actividad reciente:** Feed de pedidos y citas
   - **Estadísticas de citas:** Próximas y tendencias

10. **Inventario** - http://localhost:5173/inventory
    - Gestión de stock
    - Alertas de productos bajos

11. **Gestión de Pagos** - http://localhost:5173/payments
    - Ver todos los pagos
    - Estados y métodos

---

## 📡 API Endpoints Principales

### Autenticación
```
POST /api/auth/register/          # Registro
POST /api/auth/login/             # Login (JWT)
POST /api/auth/token/refresh/     # Refresh token
GET  /api/auth/profile/           # Perfil usuario
```

### Productos
```
GET    /api/products/             # Listar productos
GET    /api/products/{id}/        # Detalle producto
POST   /api/products/             # Crear (staff)
PUT    /api/products/{id}/        # Actualizar (staff)
DELETE /api/products/{id}/        # Eliminar (staff)
```

### Mascotas
```
GET  /api/pets/                   # Mis mascotas
POST /api/pets/                   # Registrar mascota
GET  /api/pets/{id}/              # Detalle
GET  /api/pets/{id}/medical_history/  # Historial médico
```

### Citas
```
GET  /api/appointments/           # Mis citas
POST /api/appointments/           # Reservar cita
GET  /api/appointments/{id}/      # Detalle
PUT  /api/appointments/{id}/      # Actualizar
```

### Pedidos
```
GET  /api/orders/                 # Mis pedidos
POST /api/orders/                 # Crear pedido
GET  /api/orders/{id}/            # Detalle
GET  /api/orders/{id}/tracking/   # Seguimiento
PUT  /api/orders/{id}/shipping-update/  # Actualizar envío (staff)
```

### Chat
```
GET  /api/chat/conversations/     # Mis conversaciones
POST /api/chat/conversations/     # Iniciar chat
GET  /api/chat/conversations/{id}/messages/  # Mensajes
POST /api/chat/messages/          # Enviar mensaje
WebSocket: ws://localhost:8000/ws/chat/{conversation_id}/
```

### Dashboard (Staff Only) 📊
```
GET /api/dashboard/stats/                    # Estadísticas generales
GET /api/dashboard/sales-over-time/          # Ventas en el tiempo
    ?period=daily|weekly|monthly
    &start_date=YYYY-MM-DD
    &end_date=YYYY-MM-DD
GET /api/dashboard/popular-products/         # Productos populares
    ?limit=10
GET /api/dashboard/appointments-stats/       # Estadísticas de citas
GET /api/dashboard/recent-activity/          # Actividad reciente
    ?limit=20
GET /api/dashboard/low-stock/                # Stock bajo
    ?threshold=10
```

---

## 🔑 Autenticación

El sistema usa **JWT (JSON Web Tokens)**:

1. **Login:** Obtener access_token y refresh_token
2. **Headers:** Todas las peticiones autenticadas deben incluir:
   ```
   Authorization: Bearer <access_token>
   ```
3. **Refresh:** Cuando el access_token expira, usar refresh_token

### Ejemplo con curl:
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Usar token
curl http://localhost:8000/api/dashboard/stats/ \
  -H "Authorization: Bearer <tu_access_token>"
```

---

## 🗄️ Base de Datos

### Estructura
- **SQLite** (desarrollo): `backend/db.sqlite3`
- **Modelos principales:**
  - User (autenticación)
  - Pet (mascotas)
  - Product (productos)
  - Order, OrderItem (pedidos)
  - Appointment (citas)
  - Payment (pagos)
  - Conversation, Message (chat)
  - MedicalRecord, Vaccine (historial médico)
  - Notification (notificaciones)

### Comandos útiles
```bash
# Ver estructura de BD
python manage.py dbshell
.schema

# Crear datos de prueba
python manage.py shell
>>> from apps.products.models import Product
>>> Product.objects.create(name="Test", price=10.00, stock=100)

# Reset BD (cuidado!)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 🎨 Tecnologías Clave

### Backend
- **Django 5.2.8** - Framework web
- **DRF 3.15.2** - API REST
- **Channels 4.2.0** - WebSocket
- **SimpleJWT 5.4.0** - Autenticación

### Frontend
- **React 19.2.0** - UI Framework
- **Vite 7.2.2** - Build tool
- **React Router 7.9.5** - Routing
- **Axios 1.13.2** - HTTP Client
- **Tailwind CSS 3.4.17** - Estilos
- **Material-UI 7.3.5** - Icons

---

## 📊 Tests - Cobertura

| Módulo | Tests | Tiempo | Estado |
|--------|-------|--------|--------|
| Chat | 18 | ~8s | ✅ PASS |
| Medical History | 26 | ~15s | ✅ PASS |
| Delivery | 18 | ~10s | ✅ PASS |
| Dashboard | 12 | ~8s | ✅ PASS |
| **Total** | **74+** | **~40s** | ✅ **PASS** |

---

## 🐛 Troubleshooting

### Error: "Port 8000 already in use"
```bash
# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Error: "No module named 'apps'"
```bash
# Asegúrate de estar en el directorio backend/
cd backend
source ../venv/bin/activate
python manage.py runserver
```

### Error: "CORS blocked"
Verificar en `backend/aqpvet/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

### Frontend no conecta con API
Verificar en frontend que las URLs apunten a `http://localhost:8000`:
```javascript
// Ejemplo en src/api/
const API_URL = 'http://localhost:8000/api';
```

---

## 📦 Estructura de Archivos Importante

```
proyectoAQPVET_CS_FINAL/
├── README.md                      # Este archivo
├── PROYECTO_COMPLETADO.md         # Documentación completa
├── TEST_REPORT.md                 # Reporte de tests
├── backend/
│   ├── db.sqlite3                 # Base de datos
│   ├── manage.py                  # CLI Django
│   ├── requirements.txt           # Dependencias Python
│   ├── apps/                      # Aplicaciones Django
│   │   ├── dashboard/            # ✨ NUEVO - Analytics
│   │   ├── chat/                 # Chat WebSocket
│   │   ├── pets/                 # Mascotas + Historial
│   │   └── ...
│   └── aqpvet/
│       └── settings.py           # Configuración
├── frontend/
│   ├── package.json              # Dependencias npm
│   ├── vite.config.js            # Config Vite
│   └── src/
│       ├── pages/
│       │   └── Dashboard.jsx    # ✨ NUEVO - Dashboard UI
│       ├── components/
│       ├── api/
│       └── routes/
└── venv/                         # Entorno virtual Python
```

---

## 🎓 Casos de Uso Implementados

✅ **CU01:** Registrarse/Login  
✅ **CU02:** Buscar productos  
✅ **CU03:** Carrito de compras  
✅ **CU04:** Pagar en línea  
✅ **CU05:** Reservar cita  
✅ **CU06:** Registrar mascota  
✅ **CU07:** Chat con veterinario (18 tests)  
✅ **CU08:** Historial de compras  
✅ **CU09:** Atender citas  
✅ **CU10:** Historial médico (26 tests)  
✅ **CU11:** Gestionar productos  
✅ **CU12:** Gestionar usuarios  
✅ **CU13:** Reportes y Dashboard (12 tests) ⭐ **NUEVO**  
✅ **CU14:** Actualizar stock  
✅ **CU15:** Delivery y seguimiento (18 tests)  
✅ **CU16:** Procesar pagos  

**Total: 16/16 completados** 🎉

---

## 📞 Soporte

- **Repositorio:** https://github.com/Piero-design/VETAQP
- **Issues:** https://github.com/Piero-design/VETAQP/issues
- **Email:** [Tu email aquí]

---

## 🚀 Deploy a Producción

### Checklist antes de producción:
- [ ] Cambiar `DEBUG = False` en settings.py
- [ ] Configurar `ALLOWED_HOSTS`
- [ ] Usar PostgreSQL en lugar de SQLite
- [ ] Configurar variables de entorno
- [ ] Habilitar HTTPS
- [ ] Configurar CORS para dominio de producción
- [ ] Setup de archivos estáticos con WhiteNoise o CDN
- [ ] Configurar logs
- [ ] Backups automatizados
- [ ] Monitoring (Sentry, etc.)

### Plataformas recomendadas:
- **Backend:** Railway, Render, Heroku, DigitalOcean
- **Frontend:** Vercel, Netlify, Cloudflare Pages
- **Database:** Railway PostgreSQL, AWS RDS, Supabase

---

**¡Disfruta desarrollando con AQPVET! 🐾**

*Última actualización: Enero 2025*
