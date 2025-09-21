@echo off
REM System Medic - Script de inicio rápido para Windows

echo 🏥 System Medic - Iniciando configuración...

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no está instalado. Por favor instala Python 3.11 o superior.
    pause
    exit /b 1
)

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo [INFO] Creando entorno virtual...
    python -m venv venv
    echo [SUCCESS] Entorno virtual creado
)

REM Activar entorno virtual
echo [INFO] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo [INFO] Instalando dependencias...
pip install -r requirements.txt

REM Crear archivo .env si no existe
if not exist ".env" (
    echo [INFO] Creando archivo de configuración...
    copy development.env.example .env
    echo [SUCCESS] Archivo .env creado. Puedes editarlo según tus necesidades.
)

REM Ejecutar migraciones
echo [INFO] Ejecutando migraciones de base de datos...
python manage.py makemigrations
python manage.py migrate

REM Recolectar archivos estáticos
echo [INFO] Recolectando archivos estáticos...
python manage.py collectstatic --noinput

REM Verificar si existe superusuario
echo [INFO] Verificando superusuario...
python manage.py shell -c "from django.contrib.auth.models import User; print('SUPERUSER_EXISTS:', User.objects.filter(is_superuser=True).exists())" > temp_check.txt
findstr "True" temp_check.txt >nul
if errorlevel 1 (
    echo [WARNING] No existe un superusuario. Creando uno...
    echo Por favor, ingresa los datos del superusuario:
    python manage.py createsuperuser
    echo [SUCCESS] Superusuario creado
) else (
    echo [SUCCESS] Superusuario ya existe
)
del temp_check.txt

REM Mostrar información de inicio
echo.
echo 🎉 ¡Configuración completada exitosamente!
echo.
echo 📋 Información del sistema:
python --version
python -c "import django; print('Django:', django.get_version())"
echo    • Base de datos: SQLite (desarrollo)
echo.
echo 🚀 Para iniciar el servidor:
echo    python manage.py runserver
echo.
echo 🌐 El sistema estará disponible en:
echo    http://127.0.0.1:8000
echo.
echo 👤 Panel de administración:
echo    http://127.0.0.1:8000/admin
echo.
echo 📚 Para más información, consulta el README.md
echo.

REM Preguntar si quiere iniciar el servidor
set /p choice="¿Quieres iniciar el servidor ahora? (y/n): "
if /i "%choice%"=="y" (
    echo [INFO] Iniciando servidor de desarrollo...
    python manage.py runserver
)

pause
