# System Medic - Sistema de Gestión de Consultorio Médico

Sistema web desarrollado en Django para la gestión integral de consultorios médicos, con control de acceso por roles y gestión completa de historias clínicas.

## 🏥 Características Principales

### 👥 Gestión de Usuarios
- **Sistema de autenticación** con roles diferenciados
- **Administradores**: Acceso completo al sistema
- **Doctores**: Acceso solo a sus pacientes y consultas
- **Control de permisos** granular por funcionalidad

### 👤 Gestión de Pacientes
- Registro completo de datos personales
- Validación de DNI y datos de contacto
- Historial médico detallado
- Búsqueda y filtrado avanzado
- Gestión de alergias y antecedentes

### 🩺 Gestión de Consultas
- Registro de consultas médicas
- Tipos de consulta (Primera, Seguimiento, Emergencia, Rutina)
- Registro de síntomas y signos vitales
- Diagnósticos con códigos ICD-10
- Tratamientos y medicamentos
- Fechas de seguimiento

### 👨‍⚕️ Gestión de Doctores
- Perfiles médicos completos
- Especialidades médicas
- Números de matrícula
- Control de acceso por especialidad

### 📊 Dashboard Inteligente
- Estadísticas en tiempo real
- Acciones rápidas
- Consultas recientes
- Información contextual por rol

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 5.0.7
- **Frontend**: Bootstrap 5.3, HTML5, CSS3, JavaScript
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Contenedores**: Docker & Docker Compose
- **Formularios**: Django Crispy Forms
- **Internacionalización**: Django i18n (Español, Inglés, Portugués)

## 📋 Requisitos del Sistema

### Desarrollo Local
- Python 3.11+
- pip
- SQLite3

### Producción con Docker
- Docker 20.0+
- Docker Compose 2.0+

## 🚀 Instalación y Configuración

### Opción 1: Desarrollo Local

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd system-medic
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   cp config_example.py .env
   # Editar .env con tus configuraciones
   ```

5. **Configurar base de datos**
   ```bash
   python setup.py
   # O manualmente:
   python manage.py makemigrations
   python manage.py migrate
   python manage.py collectstatic
   ```

6. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecutar servidor**
   ```bash
   python manage.py runserver
   ```

### Opción 2: Con Docker

1. **Desarrollo con Docker**
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```

2. **Producción con Docker**
   ```bash
   docker-compose up --build
   ```

## 🔧 Configuración de Base de Datos

### SQLite (Desarrollo Local)
```python
# En .env
USE_POSTGRES=False
```

### PostgreSQL (Docker/Producción)
```python
# En .env
USE_POSTGRES=True
DB_NAME=medic_db
DB_USER=medic_user
DB_PASSWORD=medic_password
DB_HOST=localhost
DB_PORT=5432
```

## 👥 Roles y Permisos

### Administrador
- ✅ Gestión completa de pacientes
- ✅ Gestión completa de doctores
- ✅ Acceso a todas las consultas
- ✅ Configuración del sistema
- ✅ Panel de administración Django

### Doctor
- ✅ Ver solo sus pacientes
- ✅ Crear y ver sus consultas
- ✅ Editar historias clínicas de sus pacientes
- ❌ Gestión de otros doctores
- ❌ Acceso a pacientes de otros doctores

## 🌐 Internacionalización

El sistema está preparado para múltiples idiomas:

- **Español** (por defecto)
- **Inglés**
- **Portugués**

Para agregar un nuevo idioma:
1. Agregar el código del idioma en `LANGUAGES` en `settings.py`
2. Ejecutar `python manage.py makemessages -l <codigo_idioma>`
3. Traducir los archivos en `locale/<codigo_idioma>/LC_MESSAGES/`
4. Ejecutar `python manage.py compilemessages`

## 📁 Estructura del Proyecto

```
system-medic/
├── crud/                   # Configuración principal de Django
│   ├── settings.py        # Configuraciones
│   ├── urls.py           # URLs principales
│   └── wsgi.py           # WSGI configuration
├── history/               # Aplicación principal
│   ├── models.py         # Modelos de datos
│   ├── views.py          # Vistas y lógica de negocio
│   ├── forms.py          # Formularios
│   ├── utils.py          # Utilidades y decoradores
│   ├── admin.py          # Configuración del admin
│   └── templates/        # Plantillas HTML
├── static/               # Archivos estáticos
│   ├── css/             # Estilos personalizados
│   └── js/              # JavaScript personalizado
├── docker-compose.yml    # Docker para producción
├── docker-compose.dev.yml # Docker para desarrollo
├── Dockerfile           # Imagen de Docker
├── requirements.txt     # Dependencias Python
└── README.md           # Este archivo
```

## 🔒 Seguridad

- **Autenticación requerida** para todas las vistas
- **Control de acceso por roles** implementado
- **Validación de formularios** en frontend y backend
- **Protección CSRF** habilitada
- **Variables de entorno** para datos sensibles
- **Validación de permisos** en cada operación

## 📱 Diseño Responsivo

- **Bootstrap 5.3** para diseño responsivo
- **Mobile-first** approach
- **Componentes adaptativos** para diferentes pantallas
- **Navegación optimizada** para móviles

## 🧪 Testing

```bash
# Ejecutar tests
python manage.py test

# Tests con cobertura
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 📊 Monitoreo y Logs

- **Logs de Django** configurados
- **Mensajes de usuario** con Bootstrap alerts
- **Validación en tiempo real** con JavaScript
- **Feedback visual** para todas las acciones

## 🚀 Despliegue

### Variables de Entorno de Producción
```bash
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
USE_POSTGRES=True
DB_NAME=medic_db
DB_USER=medic_user
DB_PASSWORD=strong-password
DB_HOST=db
DB_PORT=5432
```

### Comandos de Despliegue
```bash
# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o consultas:
- Crear un issue en el repositorio
- Contactar al equipo de desarrollo

## 🔄 Changelog

### v1.0.0
- ✅ Sistema de autenticación con roles
- ✅ Gestión completa de pacientes
- ✅ Gestión de consultas médicas
- ✅ Gestión de doctores
- ✅ Dashboard interactivo
- ✅ Diseño responsivo
- ✅ Soporte multilingüe
- ✅ Configuración Docker
- ✅ Validaciones y seguridad

---

**System Medic** - Desarrollado con ❤️ para mejorar la gestión de consultorios médicos.