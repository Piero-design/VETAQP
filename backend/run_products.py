import os
import sys
import django

# Ruta absoluta a la carpeta backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Añadir BACKEND al PYTHONPATH
sys.path.insert(0, BASE_DIR)

# Cambiar el directorio de ejecución al backend
os.chdir(BASE_DIR)

# Apuntar al settings.py correcto
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aqpvet.settings")

# Inicializar Django
django.setup()

print(">>> Ejecutando load_products.py ...")

# Ejecutar script
exec(open(os.path.join(BASE_DIR, "load_products.py")).read())

print(">>> Finalizado correctamente.")
