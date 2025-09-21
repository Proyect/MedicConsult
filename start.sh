#!/bin/bash

# System Medic - Script de inicio rápido

echo "🏥 System Medic - Iniciando configuración..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar mensajes
print_message() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 no está instalado. Por favor instala Python 3.11 o superior."
    exit 1
fi

# Verificar versión de Python
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.11"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    print_warning "Se recomienda Python 3.11 o superior. Versión actual: $PYTHON_VERSION"
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    print_message "Creando entorno virtual..."
    python3 -m venv venv
    print_success "Entorno virtual creado"
fi

# Activar entorno virtual
print_message "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
print_message "Instalando dependencias..."
pip install -r requirements.txt

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    print_message "Creando archivo de configuración..."
    cp development.env.example .env
    print_success "Archivo .env creado. Puedes editarlo según tus necesidades."
fi

# Ejecutar migraciones
print_message "Ejecutando migraciones de base de datos..."
python manage.py makemigrations
python manage.py migrate

# Recolectar archivos estáticos
print_message "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Verificar si existe superusuario
SUPERUSER_EXISTS=$(python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())" 2>/dev/null)

if [ "$SUPERUSER_EXISTS" = "False" ]; then
    print_warning "No existe un superusuario. Creando uno..."
    echo "Por favor, ingresa los datos del superusuario:"
    python manage.py createsuperuser
    print_success "Superusuario creado"
else
    print_success "Superusuario ya existe"
fi

# Mostrar información de inicio
echo ""
echo "🎉 ¡Configuración completada exitosamente!"
echo ""
echo "📋 Información del sistema:"
echo "   • Python: $(python --version)"
echo "   • Django: $(python -c 'import django; print(django.get_version())')"
echo "   • Base de datos: SQLite (desarrollo)"
echo ""
echo "🚀 Para iniciar el servidor:"
echo "   python manage.py runserver"
echo ""
echo "🌐 El sistema estará disponible en:"
echo "   http://127.0.0.1:8000"
echo ""
echo "👤 Panel de administración:"
echo "   http://127.0.0.1:8000/admin"
echo ""
echo "📚 Para más información, consulta el README.md"
echo ""

# Preguntar si quiere iniciar el servidor
read -p "¿Quieres iniciar el servidor ahora? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_message "Iniciando servidor de desarrollo..."
    python manage.py runserver
fi
