@echo off
REM MedicConsult - Script de Inicio Rápido para Docker

echo ========================================
echo    MedicConsult - Inicio con Docker
echo ========================================
echo.

REM Verificar que Docker esté ejecutándose
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker no está ejecutándose. Por favor inicia Docker Desktop.
    pause
    exit /b 1
)

echo ✅ Docker está ejecutándose

REM Verificar archivos necesarios
if not exist "docker-compose.yml" (
    echo ❌ Archivo docker-compose.yml no encontrado
    pause
    exit /b 1
)

if not exist "docker.env" (
    echo ❌ Archivo docker.env no encontrado
    pause
    exit /b 1
)

if not exist "Dockerfile" (
    echo ❌ Archivo Dockerfile no encontrado
    pause
    exit /b 1
)

echo ✅ Archivos de configuración encontrados

REM Crear directorios necesarios
if not exist "ssl" mkdir ssl
if not exist "backups" mkdir backups
if not exist "media" mkdir media
if not exist "staticfiles" mkdir staticfiles
if not exist "logs" mkdir logs

echo ✅ Directorios creados

REM Detener contenedores existentes
echo.
echo 🛑 Deteniendo contenedores existentes...
docker-compose down

REM Construir y ejecutar
echo.
echo 🔨 Construyendo imágenes...
docker-compose build --no-cache

if errorlevel 1 (
    echo ❌ Error construyendo imágenes
    pause
    exit /b 1
)

echo ✅ Imágenes construidas correctamente

echo.
echo 🚀 Iniciando servicios...
docker-compose up -d

if errorlevel 1 (
    echo ❌ Error iniciando servicios
    pause
    exit /b 1
)

echo ✅ Servicios iniciados

echo.
echo ⏳ Esperando que los servicios estén listos...
timeout /t 10 /nobreak >nul

REM Verificar estado
echo.
echo 📊 Estado de los servicios:
docker-compose ps

echo.
echo ========================================
echo    🎉 MedicConsult está listo!
echo ========================================
echo.
echo 🌐 Aplicación: http://localhost
echo 👤 Usuario: admin
echo 🔑 Contraseña: admin123
echo.
echo 📋 Comandos útiles:
echo    Ver logs: docker-compose logs -f
echo    Detener: docker-compose down
echo    Reiniciar: docker-compose restart
echo.
echo Presiona cualquier tecla para abrir la aplicación...
pause >nul

REM Abrir navegador
start http://localhost

echo.
echo ✅ Aplicación abierta en el navegador
echo.
echo Para detener la aplicación, ejecuta: docker-compose down
pause
