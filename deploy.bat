@echo off
REM MedicConsult - Script de Despliegue para Windows
REM Uso: deploy.bat [environment] [action]

setlocal enabledelayedexpansion

REM Variables
set ENVIRONMENT=%1
if "%ENVIRONMENT%"=="" set ENVIRONMENT=production

set ACTION=%2
if "%ACTION%"=="" set ACTION=deploy

set PROJECT_NAME=medicconsult
set COMPOSE_FILE=docker-compose.yml
set ENV_FILE=production.env

echo [%date% %time%] === MedicConsult Deployment Script ===
echo Environment: %ENVIRONMENT%
echo Action: %ACTION%

REM Verificar que Docker esté instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo [%date% %time%] ❌ Docker no está instalado. Por favor instala Docker primero.
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [%date% %time%] ❌ Docker Compose no está instalado. Por favor instala Docker Compose primero.
    exit /b 1
)

echo [%date% %time%] ✅ Docker y Docker Compose están instalados

REM Verificar archivos necesarios
if not exist "%COMPOSE_FILE%" (
    echo [%date% %time%] ❌ Archivo requerido no encontrado: %COMPOSE_FILE%
    exit /b 1
)

if not exist "%ENV_FILE%" (
    echo [%date% %time%] ❌ Archivo requerido no encontrado: %ENV_FILE%
    exit /b 1
)

if not exist "Dockerfile" (
    echo [%date% %time%] ❌ Archivo requerido no encontrado: Dockerfile
    exit /b 1
)

if not exist "requirements.txt" (
    echo [%date% %time%] ❌ Archivo requerido no encontrado: requirements.txt
    exit /b 1
)

echo [%date% %time%] ✅ Todos los archivos necesarios están presentes

REM Crear directorios necesarios
echo [%date% %time%] Creando directorios necesarios...
if not exist "ssl" mkdir ssl
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups
echo [%date% %time%] ✅ Directorios creados

REM Ejecutar acción según el parámetro
if "%ACTION%"=="deploy" goto :deploy
if "%ACTION%"=="start" goto :start
if "%ACTION%"=="stop" goto :stop
if "%ACTION%"=="restart" goto :restart
if "%ACTION%"=="status" goto :status
if "%ACTION%"=="logs" goto :logs
if "%ACTION%"=="backup" goto :backup
if "%ACTION%"=="cleanup" goto :cleanup
if "%ACTION%"=="help" goto :help
goto :invalid_action

:deploy
echo [%date% %time%] Construyendo imágenes Docker...
docker-compose -f %COMPOSE_FILE% --env-file %ENV_FILE% build --no-cache
if errorlevel 1 (
    echo [%date% %time%] ❌ Error construyendo imágenes
    exit /b 1
)

echo [%date% %time%] Iniciando servicios...
docker-compose -f %COMPOSE_FILE% --env-file %ENV_FILE% up -d
if errorlevel 1 (
    echo [%date% %time%] ❌ Error iniciando servicios
    exit /b 1
)

echo [%date% %time%] Verificando estado de los servicios...
docker-compose -f %COMPOSE_FILE% --env-file %ENV_FILE% ps

echo [%date% %time%] ✅ Despliegue completado exitosamente!
echo [%date% %time%] La aplicación está disponible en: http://localhost
echo [%date% %time%] Credenciales: admin / admin123
goto :end

:start
echo [%date% %time%] Iniciando servicios...
docker-compose -f %COMPOSE_FILE% --env-file %ENV_FILE% up -d
if errorlevel 1 (
    echo [%date% %time%] ❌ Error iniciando servicios
    exit /b 1
)
echo [%date% %time%] ✅ Servicios iniciados
goto :end

:stop
echo [%date% %time%] Deteniendo servicios...
docker-compose -f %COMPOSE_FILE% --env-file %ENV_FILE% down
echo [%date% %time%] ✅ Servicios detenidos
goto :end

:restart
echo [%date% %time%] Reiniciando servicios...
docker-compose -f %COMPOSE_FILE% --env-file %ENV_FILE% restart
echo [%date% %time%] ✅ Servicios reiniciados
goto :end

:status
echo [%date% %time%] Verificando estado de los servicios...
docker-compose -f %COMPOSE_FILE% --env-file %ENV_FILE% ps
goto :end

:logs
echo [%date% %time%] Mostrando logs de los servicios...
docker-compose -f %COMPOSE_FILE% --env-file %ENV_FILE% logs -f
goto :end

:backup
echo [%date% %time%] Creando backup de la base de datos...
set BACKUP_FILE=backups\medicconsult_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.sql
set BACKUP_FILE=!BACKUP_FILE: =0!
docker-compose -f %COMPOSE_FILE% --env-file %ENV_FILE% exec -T db pg_dump -U medic_user medic_db > "!BACKUP_FILE!"
echo [%date% %time%] ✅ Backup creado: !BACKUP_FILE!
goto :end

:cleanup
echo [%date% %time%] Limpiando recursos no utilizados...
docker system prune -f
docker volume prune -f
echo [%date% %time%] ✅ Limpieza completada
goto :end

:help
echo MedicConsult - Script de Despliegue para Windows
echo.
echo Uso: deploy.bat [environment] [action]
echo.
echo Environments:
echo   production  - Despliegue en producción (default)
echo   development - Despliegue en desarrollo
echo.
echo Actions:
echo   deploy      - Desplegar la aplicación (default)
echo   start       - Iniciar servicios
echo   stop        - Detener servicios
echo   restart     - Reiniciar servicios
echo   status      - Verificar estado de servicios
echo   logs        - Mostrar logs
echo   backup      - Crear backup de la base de datos
echo   cleanup     - Limpiar recursos no utilizados
echo   help        - Mostrar esta ayuda
echo.
echo Ejemplos:
echo   deploy.bat production deploy
echo   deploy.bat production backup
goto :end

:invalid_action
echo [%date% %time%] ❌ Acción no válida: %ACTION%
echo Use 'deploy.bat help' para ver las opciones disponibles
exit /b 1

:end
endlocal
