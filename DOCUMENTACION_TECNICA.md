# 📋 Documentación Técnica - System Medic

## 🏥 Descripción del Sistema

**System Medic** es un sistema web de gestión integral para consultorios médicos desarrollado en Django 5.0.7. Proporciona una solución completa para la administración de pacientes, consultas médicas, doctores e historias clínicas con control de acceso por roles.

## 🛠️ Arquitectura Técnica

### **Stack Tecnológico**
- **Backend:** Django 5.0.7 (Python 3.13.3)
- **Frontend:** Bootstrap 5.3, HTML5, CSS3, JavaScript ES6
- **Base de Datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Formularios:** Django Crispy Forms + Bootstrap 5
- **Contenedores:** Docker & Docker Compose
- **Internacionalización:** Django i18n (Español, Inglés, Portugués)

### **Estructura del Proyecto**
```
system-medic/
├── crud/                   # Configuración principal de Django
│   ├── settings.py        # Configuraciones del proyecto
│   ├── urls.py           # URLs principales
│   ├── wsgi.py           # WSGI configuration
│   └── asgi.py           # ASGI configuration
├── history/               # Aplicación principal
│   ├── models.py         # Modelos de datos
│   ├── views.py          # Vistas y lógica de negocio
│   ├── forms.py          # Formularios
│   ├── utils.py          # Utilidades y decoradores
│   ├── admin.py          # Configuración del admin
│   ├── apps.py           # Configuración de la app
│   ├── tests.py          # Tests unitarios
│   ├── migrations/       # Migraciones de base de datos
│   └── templates/        # Plantillas HTML
│       ├── auth/         # Plantillas de autenticación
│       ├── patients/     # Plantillas de pacientes
│       ├── consults/     # Plantillas de consultas
│       └── doctors/      # Plantillas de doctores
├── static/               # Archivos estáticos
│   ├── css/             # Estilos personalizados
│   └── js/              # JavaScript personalizado
├── .venv/               # Entorno virtual
├── requirements.txt     # Dependencias de producción
├── requirements-dev.txt # Dependencias de desarrollo
├── docker-compose.yml   # Docker para producción
├── docker-compose.dev.yml # Docker para desarrollo
├── Dockerfile          # Imagen de Docker
└── manage.py           # Script de gestión de Django
```

## 🗄️ Modelos de Datos

### **1. Person (Pacientes)**
```python
class Person(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()
    observations = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### **2. Doctor (Doctores)**
```python
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=20, unique=True)
    specialty = models.CharField(max_length=10, choices=SPECIALTY_CHOICES)
    phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### **3. Consult (Consultas)**
```python
class Consult(models.Model):
    patient = models.ForeignKey(Person, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    consult_type = models.CharField(max_length=10, choices=CONSULT_TYPE_CHOICES)
    reason = models.TextField()
    symptoms = models.TextField()
    vital_signs = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### **4. Diagnosis (Diagnósticos)**
```python
class Diagnosis(models.Model):
    consult = models.OneToOneField(Consult, on_delete=models.CASCADE)
    description = models.TextField()
    icd_code = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### **5. Treatment (Tratamientos)**
```python
class Treatment(models.Model):
    consult = models.OneToOneField(Consult, on_delete=models.CASCADE)
    description = models.TextField()
    medications = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    follow_up_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### **6. MedicalRecord (Historia Clínica)**
```python
class MedicalRecord(models.Model):
    patient = models.OneToOneField(Person, on_delete=models.CASCADE)
    allergies = models.TextField(blank=True, null=True)
    chronic_conditions = models.TextField(blank=True, null=True)
    family_history = models.TextField(blank=True, null=True)
    social_history = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## 🔐 Sistema de Autenticación y Roles

### **Roles del Sistema**

#### **Administrador**
- Acceso completo al sistema
- Gestión de todos los pacientes
- Gestión de todos los doctores
- Acceso a todas las consultas
- Configuración del sistema
- Panel de administración Django

#### **Doctor**
- Acceso solo a sus pacientes (con consultas previas)
- Crear y ver sus consultas
- Editar historias clínicas de sus pacientes
- No puede gestionar otros doctores
- No puede acceder a pacientes de otros doctores

### **Decoradores de Seguridad**
```python
@require_role('administrator')  # Solo administradores
@require_role('doctor')         # Solo doctores
@require_role('any')           # Cualquier usuario autenticado
```

## 🎨 Frontend y UI

### **Tecnologías Frontend**
- **Bootstrap 5.3:** Framework CSS responsivo
- **Bootstrap Icons:** Iconografía consistente
- **CSS3 Personalizado:** Tema médico específico
- **JavaScript ES6:** Funcionalidades interactivas

### **Características de Diseño**
- **Tema Médico:** Colores específicos del sector salud
- **Diseño Responsivo:** Mobile-first approach
- **Accesibilidad:** Cumple estándares WCAG
- **UX Optimizada:** Interacciones fluidas y intuitivas

### **Componentes Personalizados**
- **Tarjetas Médicas:** Con bordes de colores y efectos hover
- **Avatares de Pacientes:** Gradientes médicos
- **Tablas Mejoradas:** Con iconos y estilos médicos
- **Badges de Consulta:** Colores específicos por tipo
- **Formularios Inteligentes:** Validación en tiempo real

## ⚙️ Configuración del Sistema

### **Variables de Entorno**
```bash
# Configuración básica
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos
USE_POSTGRES=False  # True para PostgreSQL
DB_NAME=medic_db
DB_USER=medic_user
DB_PASSWORD=medic_password
DB_HOST=localhost
DB_PORT=5432
```

### **Configuración de Base de Datos**

#### **SQLite (Desarrollo)**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### **PostgreSQL (Producción)**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
```

## 🚀 Instalación y Despliegue

### **Desarrollo Local**
```bash
# 1. Clonar repositorio
git clone <repository-url>
cd system-medic

# 2. Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements-dev.txt

# 4. Configurar base de datos
python manage.py makemigrations
python manage.py migrate

# 5. Crear superusuario
python manage.py createsuperuser

# 6. Ejecutar servidor
python manage.py runserver
```

### **Producción con Docker**
```bash
# Desarrollo
docker-compose -f docker-compose.dev.yml up --build

# Producción
docker-compose up --build
```

## 🧪 Testing

### **Ejecutar Tests**
```bash
# Tests básicos
python manage.py test

# Tests con cobertura
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### **Tests Disponibles**
- Tests unitarios de modelos
- Tests de vistas y formularios
- Tests de autenticación y permisos
- Tests de integración

## 📊 Monitoreo y Logs

### **Configuración de Logs**
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 🔒 Seguridad

### **Medidas Implementadas**
- **Autenticación requerida** para todas las vistas
- **Control de acceso por roles** granular
- **Validación de formularios** frontend y backend
- **Protección CSRF** habilitada
- **Variables de entorno** para datos sensibles
- **Validación de permisos** en cada operación
- **Sanitización de datos** de entrada

### **Buenas Prácticas**
- Contraseñas seguras obligatorias
- Sesiones con timeout automático
- Validación de entrada en todos los formularios
- Escape de datos en plantillas
- Headers de seguridad configurados

## 🌐 Internacionalización

### **Idiomas Soportados**
- **Español** (por defecto)
- **Inglés**
- **Portugués**

### **Configuración**
```python
LANGUAGE_CODE = 'es'
LANGUAGES = [
    ('es', 'Español'),
    ('en', 'English'),
    ('pt', 'Português'),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
```

## 📱 API y Integraciones

### **Endpoints Disponibles**
- `/admin/` - Panel de administración Django
- `/login/` - Autenticación
- `/dashboard/` - Panel principal
- `/patients/` - Gestión de pacientes
- `/consults/` - Gestión de consultas
- `/doctors/` - Gestión de doctores

### **Formato de Respuesta**
```json
{
    "status": "success",
    "data": {...},
    "message": "Operación exitosa"
}
```

## 🔧 Mantenimiento

### **Comandos de Mantenimiento**
```bash
# Recolectar archivos estáticos
python manage.py collectstatic

# Limpiar sesiones expiradas
python manage.py clearsessions

# Verificar integridad de la base de datos
python manage.py check --deploy

# Crear backup de la base de datos
python manage.py dumpdata > backup.json
```

### **Monitoreo de Rendimiento**
- Logs de acceso y errores
- Métricas de uso de la base de datos
- Monitoreo de memoria y CPU
- Alertas de seguridad

## 📈 Escalabilidad

### **Optimizaciones Implementadas**
- **Paginación** en listas largas
- **Índices de base de datos** en campos críticos
- **Caché de consultas** frecuentes
- **Compresión de archivos estáticos**
- **Lazy loading** de imágenes

### **Consideraciones para Escalamiento**
- Migración a PostgreSQL para producción
- Implementación de Redis para caché
- Uso de CDN para archivos estáticos
- Load balancing para múltiples instancias
- Monitoreo con herramientas como Prometheus

## 🐛 Troubleshooting

### **Problemas Comunes**

#### **Error de Entorno Virtual**
```bash
# Solución: Activar entorno virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

#### **Error de Migraciones**
```bash
# Solución: Recrear migraciones
python manage.py makemigrations
python manage.py migrate
```

#### **Error de Dependencias**
```bash
# Solución: Reinstalar dependencias
pip install -r requirements-dev.txt
```

## 📞 Soporte Técnico

### **Recursos de Ayuda**
- Documentación oficial de Django
- Stack Overflow para problemas específicos
- Issues en el repositorio del proyecto
- Comunidad de desarrolladores Django

### **Contacto**
- **Desarrollador:** [Tu Nombre]
- **Email:** [tu-email@ejemplo.com]
- **Repositorio:** [URL del repositorio]

---

**System Medic** - Desarrollado con ❤️ para mejorar la gestión de consultorios médicos.

