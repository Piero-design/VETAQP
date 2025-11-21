# TEST_REPORT

Proyecto: AQPVET (proyectoAQPVET_CS_FINAL)

Fecha de ejecución: 19 de noviembre de 2025

---

## Herramientas usadas
- Backend: Django 5.1.3
- API: Django REST Framework
- Autenticación: djangorestframework-simplejwt (JWT)
- Runner de tests: Django test runner (unittest)
- Pruebas de integración: `rest_framework.test.APITestCase`
- Pruebas de sistema: `django.test.LiveServerTestCase` + `requests`
- Frontend (para evidencias manuales): Vite + React

---

## Archivos de tests añadidos
- `backend/apps/users/tests_integration.py` (3 tests)
- `backend/apps/pets/tests_integration.py` (3 tests)
- `backend/apps/products/tests_integration.py` (2 tests)
- `backend/tests_system.py` (5 system tests)

Total implementado:
- Pruebas de integración: 8 (>=5 requerido)
- Pruebas de sistema: 5 (>=5 requerido)

---

## Comandos ejecutados (copiar/pegar desde terminal)
1. Activar virtualenv
```
cd /Users/piero.o/Documents/GitHub/AQPVET/proyectoAQPVET_CS_FINAL
source venv/bin/activate
```
2. Arrancar backend (opcional para pruebas manuales)
```
cd backend
python manage.py runserver
```
3. Arrancar frontend (opcional para pruebas manuales)
```
cd frontend
npm install   # si no estaba instalado
npm run dev
```
4. Ejecutar tests y guardar salida (evidencia)
```
cd backend
python manage.py test -v 2 | tee ~/aqpvet-test-results.txt
```
o ejecutar sólo los tests añadidos
```
python manage.py test apps.users.tests_integration apps.pets.tests_integration apps.products.tests_integration tests_system -v 2 | tee ~/aqpvet-test-results-selected.txt
```

---

## Evidencias generadas
- Salida completa de tests: `~/aqpvet-test-results.txt` (o `~/aqpvet-test-results-selected.txt`)
- Captura terminal: `~/Desktop/aqpvet_terminal.png` (sugerido)
- Captura frontend: `~/Desktop/aqpvet_frontend.png` (sugerido)
- Log Vite (opcional): `~/vite.log`

Si no tienes las capturas en esas rutas, indica las rutas que usaste y las actualizo en el informe.

---

## Resultados obtenidos (resumen)
Tras ejecutar los tests se obtuvieron los siguientes resultados (captura parcial de la salida que pegaste):

```
Found 9 test(s).
...
Ran 9 tests in 1.857s

FAILED (failures=1, errors=1)
```

Detalle de los problemas detectados en esa ejecución:
- Error (ImportError): `ModuleNotFoundError: No module named 'requests'` — esto ocurrió al ejecutar las pruebas de sistema porque `requests` no estaba instalado en el `venv`. Solución: `pip install requests`.
- Fallo (assertion): `test_create_pet_authenticated` en `apps.pets.tests_integration` — inicialmente provocaba `401` cuando intentábamos usar `client.login()`; se corrigió actualizando el test para autenticarse con JWT (usar `/api/auth/login/` y poner `Authorization: Bearer <token>`).

Después de instalar `requests` y actualizar el test de pets para usar JWT, vuelve a ejecutar los tests. El resultado esperado es que todos los tests pasen; si aún queda alguna falla, pegar la salida completa y la depuramos.

---

## Observaciones y próximos pasos recomendados
1. Verificar que `requests` está instalado en el `venv` (ejecutar `pip install requests`).
2. Volver a ejecutar todos los tests y guardar salida con `tee`.
3. Adjuntar las capturas solicitadas en el apartado *Evidencias* (terminal y frontend). Si quieres, puedo añadir un ZIP con las rutas listadas.
4. Si quieres que deje el informe completamente terminado con la salida final (pasó OK), pega aquí las últimas 20 líneas de `~/aqpvet-test-results.txt` y las rutas reales de tus capturas; yo actualizo `TEST_REPORT.md` con los resultados finales y el estado "PASSED".

---

Si quieres que actualice ahora el informe con la salida final, pega aquí el contenido (o las últimas 20 líneas) de `~/aqpvet-test-results.txt` y las rutas de las capturas; lo incorporo automáticamente.
