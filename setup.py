#!/usr/bin/env python
"""
Script de configuración inicial para System Medic
"""
import os
import sys
import django
from pathlib import Path

def setup_django():
    """Configurar Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crud.settings')
    django.setup()

def create_migrations():
    """Crear migraciones"""
    from django.core.management import execute_from_command_line
    print("Creando migraciones...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'makemigrations', 'history'])

def run_migrations():
    """Ejecutar migraciones"""
    from django.core.management import execute_from_command_line
    print("Ejecutando migraciones...")
    execute_from_command_line(['manage.py', 'migrate'])

def create_superuser():
    """Crear superusuario"""
    from django.core.management import execute_from_command_line
    print("Creando superusuario...")
    execute_from_command_line(['manage.py', 'createsuperuser'])

def collect_static():
    """Recolectar archivos estáticos"""
    from django.core.management import execute_from_command_line
    print("Recolectando archivos estáticos...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])

def main():
    """Función principal"""
    print("=== System Medic - Configuración Inicial ===")
    
    try:
        setup_django()
        create_migrations()
        run_migrations()
        collect_static()
        
        print("\n✅ Configuración completada exitosamente!")
        print("\nPara crear un superusuario, ejecuta:")
        print("python manage.py createsuperuser")
        print("\nPara ejecutar el servidor, usa:")
        print("python manage.py runserver")
        
    except Exception as e:
        print(f"❌ Error durante la configuración: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
