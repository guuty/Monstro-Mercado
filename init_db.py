#!/usr/bin/env python
"""
Script para inicializar la base de datos en Render
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.sites.models import Site

# Crear o actualizar el Site para django-allauth
site, created = Site.objects.get_or_create(
    id=1,
    defaults={
        'domain': os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'localhost'),
        'name': 'Monstro Mercado'
    }
)

if not created:
    # Actualizar si ya existe
    site.domain = os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'localhost')
    site.name = 'Monstro Mercado'
    site.save()
    print(f"✅ Site actualizado: {site.domain}")
else:
    print(f"✅ Site creado: {site.domain}")

print("✅ Base de datos inicializada correctamente")