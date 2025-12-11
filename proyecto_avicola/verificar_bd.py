#!/usr/bin/env python
"""
Script para verificar la conexión a la BD y estado de las migraciones
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_raciones.settings')
django.setup()

from django.db import connections
from django.core.management import call_command
from django.core.management.color import no_style
from panel.models import Insumo, LoteGallinas, Racion, AlertaStock, ConfiguracionUsuario

def verificar_conexion():
    """Verifica que puedas conectarte a la BD"""
    print("=" * 60)
    print("🔍 VERIFICANDO CONEXIÓN A LA BASE DE DATOS")
    print("=" * 60)
    
    try:
        db_conn = connections['default']
        db_conn.ensure_connection()
        print("✓ Conexión exitosa a MySQL")
        print(f"  - Engine: {db_conn.settings_dict['ENGINE']}")
        print(f"  - Host: {db_conn.settings_dict['HOST']}")
        print(f"  - Base de datos: {db_conn.settings_dict['NAME']}")
        print(f"  - Puerto: {db_conn.settings_dict['PORT']}")
        return True
    except Exception as e:
        print(f"✗ Error de conexión: {e}")
        return False

def verificar_modelos():
    """Verifica que los modelos existan en la BD"""
    print("\n" + "=" * 60)
    print("📋 VERIFICANDO MODELOS EN LA BD")
    print("=" * 60)
    
    modelos = [
        ("Insumo", Insumo),
        ("LoteGallinas", LoteGallinas),
        ("Racion", Racion),
        ("AlertaStock", AlertaStock),
        ("ConfiguracionUsuario", ConfiguracionUsuario),
    ]
    
    for nombre, modelo in modelos:
        try:
            count = modelo.objects.count()
            print(f"✓ {nombre}: {count} registros")
        except Exception as e:
            print(f"✗ {nombre}: Error - {e}")

def mostrar_insumos():
    """Muestra los insumos registrados"""
    print("\n" + "=" * 60)
    print("📦 INSUMOS REGISTRADOS")
    print("=" * 60)
    
    try:
        insumos = Insumo.objects.all()
        if insumos.exists():
            for insumo in insumos:
                print(f"  • {insumo.nombre}: {insumo.stock_actual} {insumo.unidad} (Mín: {insumo.stock_minimo})")
        else:
            print("  ⚠️  No hay insumos registrados aún.")
            print("  Usa la interfaz para crear uno.")
    except Exception as e:
        print(f"  ✗ Error al leer insumos: {e}")

if __name__ == "__main__":
    print("\n🚀 INICIO DE VERIFICACIÓN\n")
    
    if verificar_conexion():
        verificar_modelos()
        mostrar_insumos()
        print("\n" + "=" * 60)
        print("✅ TODO ESTÁ CORRECTAMENTE CONFIGURADO")
        print("=" * 60 + "\n")
    else:
        print("\n❌ NO SE PUEDE CONECTAR A LA BD")
        print("Revisa los datos en settings.py\n")
        sys.exit(1)
