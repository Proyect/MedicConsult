# MedicConsult - Guía de Despliegue

## 📋 Índice
- [Requisitos del Sistema](#requisitos-del-sistema)
- [Configuración Inicial](#configuración-inicial)
- [Despliegue Local](#despliegue-local)
- [Despliegue en Producción](#despliegue-en-producción)
- [Configuración de Variables de Entorno](#configuración-de-variables-de-entorno)
- [Comandos de Gestión](#comandos-de-gestión)
- [Monitoreo y Mantenimiento](#monitoreo-y-mantenimiento)
- [Solución de Problemas](#solución-de-problemas)

## 🖥️ Requisitos del Sistema

### Mínimos
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **RAM**: 2GB
- **Disco**: 10GB libres
- **CPU**: 2 cores

### Recomendados
- **Docker**: 24.0+
- **Docker Compose**: 2.20+
- **RAM**: 4GB+
- **Disco**: 20GB+ libres
- **CPU**: 4+ cores

## ⚙️ Configuración Inicial

### 1. Clonar el Repositorio
```bash
git clone <repository-url>
cd MedicConsult
```

### 2. Configurar Variables de Entorno
```bash
# Copiar archivo de ejemplo
cp production.env .env

# Editar variables según tu entorno
nano .env
```

### 3. Verificar Archivos Necesarios
```bash
# Verificar que todos los archivos estén presentes
ls -la
# Debe incluir: Dockerfile, docker-compose.yml, production.env, deploy.sh
```

## 🚀 Despliegue Local

### Opción 1: Script Automático (Recomendado)
```bash
# Dar permisos de ejecución
chmod +x deploy.sh

# Desplegar aplicación completa
./deploy.sh production deploy

# O usar Make
make deploy
```

### Opción 2: Comandos Manuales
```bash
# Construir imágenes
docker-compose -f docker-compose.yml --env-file production.env build

# Iniciar servicios
docker-compose -f docker-compose.yml --env-file production.env up -d

# Verificar estado
docker-compose -f docker-compose.yml --env-file production.env ps
```

### Opción 3: Desarrollo Local
```bash
# Activar entorno virtual
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

## 🌐 Despliegue en Producción

### 1. Configurar Servidor
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
```

### 2. Configurar Variables de Producción
```bash
# Editar variables de producción
nano production.env

# Cambiar valores críticos:
# - SECRET_KEY (generar uno nuevo)
# - DB_PASSWORD (contraseña segura)
# - ALLOWED_HOSTS (tu dominio)
# - DEBUG=False
```

### 3. Desplegar
```bash
# Desplegar aplicación
./deploy.sh production deploy

# Verificar estado
make status
```

### 4. Configurar SSL (Opcional)
```bash
# Crear directorio para certificados
mkdir ssl

# Copiar certificados SSL
cp your-cert.pem ssl/cert.pem
cp your-key.pem ssl/key.pem

# Editar nginx.conf para habilitar HTTPS
# Descomentar sección HTTPS en nginx.conf
```

## 🔧 Configuración de Variables de Entorno

### Variables Principales
```bash
# Base de datos
DB_NAME=medic_db
DB_USER=medic_user
DB_PASSWORD=tu_contraseña_segura
DB_HOST=db
DB_PORT=5432

# Django
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,tu-dominio.com

# Puertos
WEB_PORT=8000
NGINX_PORT=80
NGINX_SSL_PORT=443

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicación
```

### Generar SECRET_KEY
```python
# En Python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## 📊 Comandos de Gestión

### Scripts de Despliegue
```bash
# Desplegar aplicación completa
./deploy.sh production deploy

# Iniciar servicios
./deploy.sh production start

# Detener servicios
./deploy.sh production stop

# Reiniciar servicios
./deploy.sh production restart

# Ver estado
./deploy.sh production status

# Ver logs
./deploy.sh production logs

# Crear backup
./deploy.sh production backup

# Restaurar backup
./deploy.sh production restore backups/archivo.sql

# Limpiar recursos
./deploy.sh production cleanup
```

### Comandos Make
```bash
# Ver todos los comandos disponibles
make help

# Desplegar
make deploy

# Gestión de servicios
make start
make stop
make restart
make status
make logs

# Backup y restauración
make backup
make restore FILE=backups/archivo.sql

# Mantenimiento
make cleanup
make health
make update
```

### Comandos Docker Directos
```bash
# Ver contenedores
docker ps

# Ver logs
docker-compose logs -f

# Ejecutar comando en contenedor
docker-compose exec web python manage.py shell

# Backup de base de datos
docker-compose exec db pg_dump -U medic_user medic_db > backup.sql

# Restaurar base de datos
docker-compose exec -T db psql -U medic_user medic_db < backup.sql
```

## 📈 Monitoreo y Mantenimiento

### Verificar Salud de la Aplicación
```bash
# Verificar estado general
make health

# Verificar logs
make logs

# Verificar recursos
docker stats
```

### Backup Automático
```bash
# Crear script de backup automático
cat > backup_auto.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backups/medicconsult_$DATE.sql"
mkdir -p backups
docker-compose exec -T db pg_dump -U medic_user medic_db > "$BACKUP_FILE"
echo "Backup creado: $BACKUP_FILE"
EOF

chmod +x backup_auto.sh

# Programar con cron (backup diario a las 2 AM)
echo "0 2 * * * /ruta/completa/backup_auto.sh" | crontab -
```

### Actualizaciones
```bash
# Actualizar dependencias
make update

# Reconstruir contenedores
docker-compose build --no-cache

# Reiniciar servicios
make restart
```

## 🔍 Solución de Problemas

### Problemas Comunes

#### 1. Error de Permisos
```bash
# Solución
chmod +x deploy.sh
chmod +x docker-entrypoint.sh
```

#### 2. Puerto en Uso
```bash
# Verificar puertos en uso
netstat -tulpn | grep :80
netstat -tulpn | grep :8000

# Cambiar puertos en production.env
NGINX_PORT=8080
WEB_PORT=8001
```

#### 3. Error de Base de Datos
```bash
# Verificar logs de base de datos
docker-compose logs db

# Reiniciar solo la base de datos
docker-compose restart db

# Verificar conexión
docker-compose exec db pg_isready -U medic_user
```

#### 4. Error de Archivos Estáticos
```bash
# Recolectar archivos estáticos
docker-compose exec web python manage.py collectstatic --noinput

# Verificar permisos
docker-compose exec web ls -la /app/staticfiles
```

#### 5. Error de Memoria
```bash
# Verificar uso de memoria
docker stats

# Limpiar recursos
make cleanup

# Aumentar memoria disponible
# Editar docker-compose.yml para agregar límites de memoria
```

### Logs Importantes
```bash
# Logs de aplicación
docker-compose logs web

# Logs de base de datos
docker-compose logs db

# Logs de nginx
docker-compose logs nginx

# Logs del sistema
tail -f logs/django.log
```

### Comandos de Diagnóstico
```bash
# Verificar configuración
docker-compose config

# Verificar salud de contenedores
docker-compose ps

# Verificar volúmenes
docker volume ls

# Verificar redes
docker network ls
```

## 📞 Soporte

### Información del Sistema
```bash
# Generar reporte del sistema
make status

# Verificar versión de Docker
docker --version
docker-compose --version

# Verificar espacio en disco
df -h

# Verificar memoria
free -h
```

### Archivos de Log
- **Aplicación**: `logs/django.log`
- **Nginx**: `docker-compose logs nginx`
- **Base de datos**: `docker-compose logs db`

### Contacto
Para soporte técnico o reportar problemas, contacta al equipo de desarrollo.

---

## 🎯 Resumen de Comandos Rápidos

```bash
# Despliegue completo
make deploy

# Gestión básica
make start
make stop
make restart
make status

# Backup y mantenimiento
make backup
make cleanup
make health

# Desarrollo
make dev
make test
make migrate
```

¡MedicConsult está listo para producción! 🚀
