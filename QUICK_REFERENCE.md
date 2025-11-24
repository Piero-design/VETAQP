# 🚀 AQPVET - Quick Reference Card

## ⚡ Quick Start Commands

### Backend
```bash
cd backend
source ../venv/bin/activate
python manage.py runserver          # Port 8000
```

### Frontend
```bash
cd frontend
npm run dev                         # Port 5173
```

### Tests
```bash
cd backend
source ../venv/bin/activate

# Dashboard tests (12)
python manage.py test apps.dashboard.tests_integration -v 2

# All tests (74+)
python manage.py test -v 2
```

---

## 🔑 Default Credentials

**Admin/Staff User:**
- Username: `admin`
- Password: `admin123`
- Access: Full dashboard + admin panel

---

## 📡 Key Endpoints

### Public
```
POST /api/auth/register/            # Register new user
POST /api/auth/login/               # Login (get JWT)
GET  /api/products/                 # List products
```

### Authenticated
```
GET  /api/auth/profile/             # User profile
GET  /api/pets/                     # My pets
GET  /api/appointments/             # My appointments
GET  /api/orders/                   # My orders
GET  /api/chat/conversations/       # My chats
```

### Staff Only (Dashboard)
```
GET  /api/dashboard/stats/                   # General stats
GET  /api/dashboard/sales-over-time/         # Sales trends
GET  /api/dashboard/popular-products/        # Top products
GET  /api/dashboard/appointments-stats/      # Appointments analytics
GET  /api/dashboard/recent-activity/         # Activity feed
GET  /api/dashboard/low-stock/               # Low stock alerts
```

---

## 🎯 Main URLs

| Feature | URL |
|---------|-----|
| Home/Catalog | http://localhost:5173/ |
| Login | http://localhost:5173/login |
| Dashboard ⭐ | http://localhost:5173/dashboard |
| Appointments | http://localhost:5173/appointments |
| Chat | http://localhost:5173/chat |
| Pets | http://localhost:5173/pets |
| Medical History | http://localhost:5173/medical-history |
| Orders | http://localhost:5173/orders |
| Order Tracking | http://localhost:5173/order-tracking |
| Inventory | http://localhost:5173/inventory |
| Payments | http://localhost:5173/payments |

---

## 🧪 Test Summary

| Module | Tests | Status |
|--------|-------|--------|
| Dashboard | 12 | ✅ PASS |
| Chat | 18 | ✅ PASS |
| Medical History | 26 | ✅ PASS |
| Delivery | 18 | ✅ PASS |
| **Total** | **74+** | ✅ **PASS** |

---

## 📁 Project Structure

```
proyectoAQPVET_CS_FINAL/
├── backend/
│   ├── apps/
│   │   ├── dashboard/      ⭐ NEW
│   │   ├── chat/
│   │   ├── pets/
│   │   └── [8 more apps]
│   ├── aqpvet/
│   └── db.sqlite3
├── frontend/
│   └── src/
│       ├── pages/
│       │   └── Dashboard.jsx  ⭐ NEW
│       ├── components/
│       └── api/
└── venv/
```

---

## 🔧 Common Commands

### Django
```bash
python manage.py makemigrations     # Create migrations
python manage.py migrate            # Apply migrations
python manage.py createsuperuser    # Create admin user
python manage.py shell              # Django shell
python manage.py dbshell            # Database shell
```

### npm
```bash
npm install                         # Install dependencies
npm run dev                         # Development server
npm run build                       # Production build
npm run preview                     # Preview build
```

---

## 🐛 Troubleshooting

### Port in use
```bash
# macOS/Linux
lsof -ti:8000 | xargs kill -9       # Backend
lsof -ti:5173 | xargs kill -9       # Frontend
```

### Database reset
```bash
cd backend
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Clear cache
```bash
# Backend
find . -name "*.pyc" -delete
find . -name "__pycache__" -delete

# Frontend
rm -rf node_modules
npm install
```

---

## 📊 Dashboard Features

1. **Overview Stats** - Total orders, revenue, users, pets
2. **Sales Trends** - Daily/weekly/monthly analysis
3. **Top Products** - Best sellers by quantity
4. **Appointments** - Stats and upcoming
5. **Activity Feed** - Recent orders + appointments
6. **Low Stock** - Inventory alerts

---

## 🔐 Authentication

**JWT Token Flow:**
1. Login → Get `access_token` + `refresh_token`
2. Add header: `Authorization: Bearer <access_token>`
3. Token expires → Use `refresh_token` to get new one

---

## ✅ Use Cases (16/16)

- [x] CU01: Register/Login
- [x] CU02: Product search
- [x] CU03: Shopping cart
- [x] CU04: Online payment
- [x] CU05: Book appointment
- [x] CU06: Register pet
- [x] CU07: Vet chat
- [x] CU08: Order history
- [x] CU09: Attend appointments
- [x] CU10: Medical history
- [x] CU11: Manage products
- [x] CU12: Manage users
- [x] CU13: Dashboard/Reports ⭐
- [x] CU14: Update stock
- [x] CU15: Delivery tracking
- [x] CU16: Process payments

---

## 📚 Documentation Files

1. `README.md` - Quick start guide
2. `PROYECTO_COMPLETADO.md` - Full project documentation
3. `DASHBOARD_DOCUMENTATION.md` - Dashboard technical docs
4. `RESUMEN_FINAL.md` - Final summary
5. `INFORME_DEBUGGING.md` - Debugging process
6. `TEST_REPORT.md` - Test results

---

## 🎯 Status

**Project:** ✅ 100% Complete  
**Tests:** ✅ 74+ Passing  
**Modules:** ✅ 10/10  
**Use Cases:** ✅ 16/16  
**Production:** ✅ Ready

---

**Version:** 1.0.0  
**Last Updated:** January 2025  
**Repository:** https://github.com/Piero-design/VETAQP
