#!/bin/bash

# MedicConsult - Script de Despliegue
# Uso: ./deploy.sh [environment] [action]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar mensajes
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] ✅${NC} $1"
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] ⚠️${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ❌${NC} $1"
}

# Variables
ENVIRONMENT=${1:-production}
ACTION=${2:-deploy}
PROJECT_NAME="medicconsult"
COMPOSE_FILE="docker-compose.yml"
ENV_FILE="production.env"

# Verificar que Docker esté instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        error "Docker no está instalado. Por favor instala Docker primero."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose no está instalado. Por favor instala Docker Compose primero."
        exit 1
    fi
    
    success "Docker y Docker Compose están instalados"
}

# Verificar archivos necesarios
check_files() {
    local files=("$COMPOSE_FILE" "$ENV_FILE" "Dockerfile" "requirements.txt")
    
    for file in "${files[@]}"; do
        if [[ ! -f "$file" ]]; then
            error "Archivo requerido no encontrado: $file"
            exit 1
        fi
    done
    
    success "Todos los archivos necesarios están presentes"
}

# Crear directorios necesarios
create_directories() {
    log "Creando directorios necesarios..."
    mkdir -p ssl logs backups
    success "Directorios creados"
}

# Construir imágenes
build_images() {
    log "Construyendo imágenes Docker..."
    docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE build --no-cache
    success "Imágenes construidas correctamente"
}

# Iniciar servicios
start_services() {
    log "Iniciando servicios..."
    docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE up -d
    success "Servicios iniciados"
}

# Detener servicios
stop_services() {
    log "Deteniendo servicios..."
    docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE down
    success "Servicios detenidos"
}

# Reiniciar servicios
restart_services() {
    log "Reiniciando servicios..."
    docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE restart
    success "Servicios reiniciados"
}

# Verificar estado de los servicios
check_services() {
    log "Verificando estado de los servicios..."
    docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE ps
}

# Ver logs
show_logs() {
    log "Mostrando logs de los servicios..."
    docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE logs -f
}

# Backup de la base de datos
backup_database() {
    log "Creando backup de la base de datos..."
    local backup_file="backups/medicconsult_$(date +%Y%m%d_%H%M%S).sql"
    
    docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE exec -T db pg_dump -U medic_user medic_db > "$backup_file"
    success "Backup creado: $backup_file"
}

# Restaurar base de datos
restore_database() {
    local backup_file=$1
    if [[ -z "$backup_file" ]]; then
        error "Debe especificar un archivo de backup"
        exit 1
    fi
    
    if [[ ! -f "$backup_file" ]]; then
        error "Archivo de backup no encontrado: $backup_file"
        exit 1
    fi
    
    log "Restaurando base de datos desde: $backup_file"
    docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE exec -T db psql -U medic_user -d medic_db < "$backup_file"
    success "Base de datos restaurada"
}

# Limpiar recursos no utilizados
cleanup() {
    log "Limpiando recursos no utilizados..."
    docker system prune -f
    docker volume prune -f
    success "Limpieza completada"
}

# Mostrar ayuda
show_help() {
    echo "MedicConsult - Script de Despliegue"
    echo ""
    echo "Uso: $0 [environment] [action]"
    echo ""
    echo "Environments:"
    echo "  production  - Despliegue en producción (default)"
    echo "  development - Despliegue en desarrollo"
    echo ""
    echo "Actions:"
    echo "  deploy      - Desplegar la aplicación (default)"
    echo "  start       - Iniciar servicios"
    echo "  stop        - Detener servicios"
    echo "  restart     - Reiniciar servicios"
    echo "  status      - Verificar estado de servicios"
    echo "  logs        - Mostrar logs"
    echo "  backup      - Crear backup de la base de datos"
    echo "  restore     - Restaurar base de datos (requiere archivo)"
    echo "  cleanup     - Limpiar recursos no utilizados"
    echo "  help        - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 production deploy"
    echo "  $0 production backup"
    echo "  $0 production restore backups/backup.sql"
}

# Función principal
main() {
    log "=== MedicConsult Deployment Script ==="
    log "Environment: $ENVIRONMENT"
    log "Action: $ACTION"
    
    case $ACTION in
        "deploy")
            check_docker
            check_files
            create_directories
            build_images
            start_services
            check_services
            success "Despliegue completado exitosamente!"
            log "La aplicación está disponible en: http://localhost"
            log "Credenciales: admin / admin123"
            ;;
        "start")
            check_docker
            start_services
            check_services
            ;;
        "stop")
            check_docker
            stop_services
            ;;
        "restart")
            check_docker
            restart_services
            check_services
            ;;
        "status")
            check_docker
            check_services
            ;;
        "logs")
            check_docker
            show_logs
            ;;
        "backup")
            check_docker
            backup_database
            ;;
        "restore")
            check_docker
            restore_database "$3"
            ;;
        "cleanup")
            cleanup
            ;;
        "help")
            show_help
            ;;
        *)
            error "Acción no válida: $ACTION"
            show_help
            exit 1
            ;;
    esac
}

# Ejecutar función principal
main "$@"
