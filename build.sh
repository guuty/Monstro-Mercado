#!/usr/bin/env bash
set -o errexit

echo "🚀 Iniciando build para Render..."

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Recolectar archivos estáticos
echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --no-input

# Aplicar migraciones
echo "🗄️  Aplicando migraciones..."
python manage.py migrate

# Inicializar base de datos (crear Site para django-allauth)
echo "🔧 Inicializando base de datos..."
python init_db.py

echo "✅ Build completado exitosamente!"