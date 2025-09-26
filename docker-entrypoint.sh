#!/bin/bash
set -e

# Función para esperar a que la base de datos esté lista
wait_for_db() {
    echo "Esperando a que la base de datos esté lista..."
    while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
        echo "Base de datos no disponible - esperando..."
        sleep 2
    done
    echo "Base de datos está lista!"
}

# Función para ejecutar migraciones
run_migrations() {
    echo "Ejecutando migraciones..."
    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
}

# Función para recolectar archivos estáticos
collect_static() {
    echo "Recolectando archivos estáticos..."
    python manage.py collectstatic --noinput
}

# Función para crear superusuario si no existe
create_superuser() {
    echo "Verificando superusuario..."
    python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@medicconsult.com', 'admin123')
    print('Superusuario creado: admin/admin123')
else:
    print('Superusuario ya existe')
"
}

# Función para crear directorios necesarios
create_directories() {
    echo "Creando directorios necesarios..."
    mkdir -p /app/staticfiles
    mkdir -p /app/media
    mkdir -p /app/logs
}

# Función principal
main() {
    echo "=== Iniciando MedicConsult ==="
    
    # Crear directorios
    create_directories
    
    # Si se especifica USE_POSTGRES, esperar a la base de datos
    if [ "$USE_POSTGRES" = "true" ]; then
        wait_for_db
    fi
    
    # Ejecutar migraciones
    run_migrations
    
    # Recolectar archivos estáticos
    collect_static
    
    # Crear superusuario si no existe
    create_superuser
    
    echo "=== MedicConsult iniciado correctamente ==="
    
    # Ejecutar el comando principal
    exec "$@"
}

# Ejecutar función principal con todos los argumentos
main "$@"
