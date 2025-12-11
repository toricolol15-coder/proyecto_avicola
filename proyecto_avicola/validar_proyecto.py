#!/usr/bin/env python
"""
Script para validar y arreglar todos los errores del proyecto
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_raciones.settings')
django.setup()

from django.db import connections
from django.core.management import call_command
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist
from panel.models import Insumo, RegistroRacion
from django.contrib.auth.models import User

def check_templates():
    """Verifica que todos los templates existan"""
    print("\n" + "=" * 60)
    print("📄 VERIFICANDO PLANTILLAS HTML")
    print("=" * 60)
    
    templates = [
        'base.html',
        'panel/dashboard.html',
        'panel/stock.html',
        'panel/stock_agregar.html',
        'panel/stock_crear.html',
        'panel/configuraciones.html',
        'panel/raciones.html',
        'panel/registros.html',
        'panel/login.html',
        'panel/register.html',
    ]
    
    for template_name in templates:
        try:
            get_template(template_name)
            print(f"✓ {template_name}")
        except TemplateDoesNotExist:
            print(f"✗ {template_name} - NO ENCONTRADO")

def check_database():
    """Verifica la conexión a BD"""
    print("\n" + "=" * 60)
    print("🗄️  VERIFICANDO BASE DE DATOS")
    print("=" * 60)
    
    try:
        db_conn = connections['default']
        db_conn.ensure_connection()
        print("✓ Conexión a MySQL exitosa")
        
        # Verifica tablas
        cursor = db_conn.cursor()
        cursor.execute("""
            SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'avicoladb'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print(f"✓ Tablas en BD: {len(tables)}")
        for table in sorted(tables):
            print(f"  - {table}")
        return True
    except Exception as e:
        print(f"✗ Error BD: {e}")
        return False

def check_models():
    """Verifica modelos"""
    print("\n" + "=" * 60)
    print("📦 VERIFICANDO MODELOS")
    print("=" * 60)
    
    try:
        insumos = Insumo.objects.count()
        registros = RegistroRacion.objects.count()
        usuarios = User.objects.count()
        
        print(f"✓ Insumos: {insumos}")
        print(f"✓ Registros de raciones: {registros}")
        print(f"✓ Usuarios: {usuarios}")
        
        if usuarios == 0:
            print("\n⚠️  No hay usuarios. Crea uno con:")
            print("   python manage.py createsuperuser")
        return True
    except Exception as e:
        print(f"✗ Error en modelos: {e}")
        return False

def check_urls():
    """Verifica que las URLs estén bien configuradas"""
    print("\n" + "=" * 60)
    print("🌐 VERIFICANDO RUTAS (URLs)")
    print("=" * 60)
    
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        patterns = [
            'dashboard',
            'stock',
            'stock_crear',
            'stock_agregar',
            'raciones',
            'registros',
            'configuraciones',
            'login',
            'logout',
        ]
        
        for pattern in patterns:
            try:
                resolver.reverse(pattern, args=[])
            except:
                try:
                    # Intenta con args=None
                    resolver.reverse(pattern)
                    print(f"✓ {pattern}")
                    continue
                except:
                    pass
            
            try:
                # Para stock_agregar necesita un ID
                if pattern == 'stock_agregar':
                    url = resolver.reverse(pattern, args=[1])
                    print(f"✓ {pattern} → {url}")
                else:
                    url = resolver.reverse(pattern)
                    print(f"✓ {pattern} → {url}")
            except Exception as e:
                print(f"✗ {pattern} → Error: {e}")
        
        return True
    except Exception as e:
        print(f"✗ Error al verificar URLs: {e}")
        return False

def check_views():
    """Verifica que las vistas funcionen"""
    print("\n" + "=" * 60)
    print("👁️  VERIFICANDO VISTAS")
    print("=" * 60)
    
    try:
        from panel import views
        
        view_functions = [
            'dashboard',
            'stock',
            'stock_crear',
            'stock_agregar',
            'raciones',
            'registros',
            'configuraciones',
            'login_view',
            'register_view',
        ]
        
        for view_name in view_functions:
            if hasattr(views, view_name):
                print(f"✓ {view_name}")
            else:
                print(f"✗ {view_name} - NO EXISTE")
        
        return True
    except Exception as e:
        print(f"✗ Error al verificar vistas: {e}")
        return False

def main():
    print("\n" + "=" * 60)
    print("🚀 VALIDACIÓN COMPLETA DEL PROYECTO")
    print("=" * 60)
    
    check_database()
    check_templates()
    check_models()
    check_urls()
    check_views()
    
    print("\n" + "=" * 60)
    print("✅ VALIDACIÓN COMPLETADA")
    print("=" * 60)
    print("\n📝 Próximos pasos:")
    print("1. Ejecuta: python manage.py runserver")
    print("2. Abre: http://127.0.0.1:8000/")
    print("3. Crea un usuario admin si es necesario")
    print("4. Prueba todas las funcionalidades\n")

if __name__ == "__main__":
    main()
