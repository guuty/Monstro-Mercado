#!/usr/bin/env bash
set -o errexit  # hace que el script se detenga si hay errores

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Recolectar archivos estáticos (para que Render los sirva correctamente)
python manage.py collectstatic --noinput