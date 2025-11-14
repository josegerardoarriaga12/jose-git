#!/bin/bash

# Script de inicio para Django en Azure
echo "🚀 INICIANDO COCO CROCHET EN AZURE..."

# 1. Crear migraciones si no existen
echo "📦 Creando migraciones..."
python manage.py makemigrations --noinput

# 2. Aplicar migraciones a la base de datos
echo "🔄 Aplicando migraciones a MySQL..."
python manage.py migrate --noinput

# 3. Recopilar archivos estáticos (CSS, JS, imágenes)
echo "🎨 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# 4. Iniciar servidor Gunicorn (OBLIGATORIO para producción)
echo "✨ Iniciando servidor Gunicorn..."
gunicorn mi_sitio_venta.wsgi --bind=0.0.0.0:$PORT --access-logfile -