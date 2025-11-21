#!/bin/bash

# Script para probar el módulo de Inventory manualmente
# Asegúrate de que el servidor Django esté corriendo en http://127.0.0.1:8000

echo "======================================"
echo "PRUEBA MANUAL DEL MÓDULO INVENTORY"
echo "======================================"
echo ""

# Colores para la salida
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Paso 1: Obtener token JWT
echo -e "${BLUE}[1/5] Obteniendo token JWT...${NC}"
TOKEN_RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}')

TOKEN=$(echo $TOKEN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['access'])" 2>/dev/null)

if [ -z "$TOKEN" ]; then
    echo "❌ Error al obtener token. Respuesta:"
    echo $TOKEN_RESPONSE | python3 -m json.tool
    exit 1
fi

echo -e "${GREEN}✓ Token obtenido${NC}"
echo "Token: ${TOKEN:0:20}..."
echo ""

# Paso 2: Verificar que hay productos disponibles
echo -e "${BLUE}[2/5] Verificando productos disponibles...${NC}"
PRODUCTS=$(curl -s http://127.0.0.1:8000/api/products/)
echo $PRODUCTS | python3 -m json.tool | head -20
echo ""

# Obtener ID del primer producto
PRODUCT_ID=$(echo $PRODUCTS | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['results'][0]['id'] if data.get('results') and len(data['results']) > 0 else '')" 2>/dev/null)

if [ -z "$PRODUCT_ID" ]; then
    echo "⚠️  No hay productos. Creando uno para la prueba..."
    # Aquí podrías crear un producto, pero por ahora usamos el ID 1
    PRODUCT_ID=1
fi

echo -e "${GREEN}✓ Usando producto ID: $PRODUCT_ID${NC}"
echo ""

# Paso 3: Listar movimientos de inventario (debe estar vacío o mostrar existentes)
echo -e "${BLUE}[3/5] Listando movimientos de inventario actuales...${NC}"
curl -s -X GET http://127.0.0.1:8000/api/inventory/movements/ \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

# Paso 4: Crear movimiento de ENTRADA (IN)
echo -e "${BLUE}[4/5] Creando movimiento de ENTRADA (+50 unidades)...${NC}"
IN_RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/api/inventory/movements/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"product\":$PRODUCT_ID,\"movement_type\":\"IN\",\"quantity\":50,\"reason\":\"Compra inicial de inventario\"}")

echo $IN_RESPONSE | python3 -m json.tool
echo ""

# Paso 5: Crear movimiento de SALIDA (OUT)
echo -e "${BLUE}[5/5] Creando movimiento de SALIDA (-10 unidades)...${NC}"
OUT_RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/api/inventory/movements/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"product\":$PRODUCT_ID,\"movement_type\":\"OUT\",\"quantity\":10,\"reason\":\"Venta al cliente\"}")

echo $OUT_RESPONSE | python3 -m json.tool
echo ""

# Paso 6: Listar movimientos finales
echo -e "${BLUE}[BONUS] Listando todos los movimientos actualizados...${NC}"
curl -s -X GET http://127.0.0.1:8000/api/inventory/movements/ \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

echo -e "${GREEN}======================================"
echo "✓ PRUEBA COMPLETADA"
echo "======================================${NC}"
echo ""
echo "Comandos individuales que puedes usar:"
echo ""
echo "1. Obtener token:"
echo "   curl -X POST http://127.0.0.1:8000/api/auth/login/ \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"username\":\"testuser\",\"password\":\"testpass123\"}'"
echo ""
echo "2. Listar movimientos:"
echo "   curl -X GET http://127.0.0.1:8000/api/inventory/movements/ \\"
echo "     -H \"Authorization: Bearer TU_TOKEN\""
echo ""
echo "3. Crear movimiento:"
echo "   curl -X POST http://127.0.0.1:8000/api/inventory/movements/ \\"
echo "     -H \"Authorization: Bearer TU_TOKEN\" \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"product\":1,\"movement_type\":\"IN\",\"quantity\":100,\"reason\":\"Reposición\"}'"
