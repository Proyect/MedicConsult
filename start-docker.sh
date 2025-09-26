#!/bin/bash

# MedicConsult - Script de Inicio Rápido para Docker

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================"
echo -e "    MedicConsult - Inicio con Docker"
echo -e "========================================${NC}"
echo

# Verificar que Docker esté ejecutándose
if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}❌ Docker no está ejecutándose. Por favor inicia Docker.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker está ejecutándose${NC}"

# Verificar archivos necesarios
files=("docker-compose.yml" "docker.env" "Dockerfile")
for file in "${files[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo -e "${RED}❌ Archivo $file no encontrado${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✅ Archivos de configuración encontrados${NC}"

# Crear directorios necesarios
directories=("ssl" "backups" "media" "staticfiles" "logs")
for dir in "${directories[@]}"; do
    mkdir -p "$dir"
done

echo -e "${GREEN}✅ Directorios creados${NC}"

# Detener contenedores existentes
echo
echo -e "${YELLOW}🛑 Deteniendo contenedores existentes...${NC}"
docker-compose down

# Construir y ejecutar
echo
echo -e "${YELLOW}🔨 Construyendo imágenes...${NC}"
docker-compose build --no-cache

echo -e "${GREEN}✅ Imágenes construidas correctamente${NC}"

echo
echo -e "${YELLOW}🚀 Iniciando servicios...${NC}"
docker-compose up -d

echo -e "${GREEN}✅ Servicios iniciados${NC}"

echo
echo -e "${YELLOW}⏳ Esperando que los servicios estén listos...${NC}"
sleep 10

# Verificar estado
echo
echo -e "${BLUE}📊 Estado de los servicios:${NC}"
docker-compose ps

echo
echo -e "${BLUE}========================================"
echo -e "    🎉 MedicConsult está listo!"
echo -e "========================================${NC}"
echo
echo -e "${GREEN}🌐 Aplicación: http://localhost${NC}"
echo -e "${GREEN}👤 Usuario: admin${NC}"
echo -e "${GREEN}🔑 Contraseña: admin123${NC}"
echo
echo -e "${BLUE}📋 Comandos útiles:${NC}"
echo -e "   Ver logs: docker-compose logs -f"
echo -e "   Detener: docker-compose down"
echo -e "   Reiniciar: docker-compose restart"
echo

# Abrir navegador (solo en Linux/Mac)
if command -v xdg-open >/dev/null 2>&1; then
    echo -e "${YELLOW}🌐 Abriendo aplicación en el navegador...${NC}"
    xdg-open http://localhost
elif command -v open >/dev/null 2>&1; then
    echo -e "${YELLOW}🌐 Abriendo aplicación en el navegador...${NC}"
    open http://localhost
fi

echo
echo -e "${GREEN}✅ Aplicación lista para usar${NC}"
echo
echo -e "${YELLOW}Para detener la aplicación, ejecuta: docker-compose down${NC}"
