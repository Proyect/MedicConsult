# 🚀 Inicio Rápido - System Medic

## ⚡ Configuración en 5 Minutos

### **1. Activar Entorno Virtual**
```bash
# Windows
.\.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### **2. Iniciar Servidor**
```bash
python manage.py runserver
```

### **3. Acceder al Sistema**
- **URL:** http://127.0.0.1:8000/
- **Usuario:** admin
- **Contraseña:** admin123

## 🎯 Primeros Pasos

### **Como Administrador:**
1. **Crear un Doctor:**
   - Ve a "Doctores" → "Nuevo Doctor"
   - Completa los datos del usuario y doctor
   - Guarda

2. **Registrar un Paciente:**
   - Ve a "Pacientes" → "Nuevo Paciente"
   - Completa todos los campos obligatorios
   - Guarda

3. **Crear una Consulta:**
   - Ve a "Consultas" → "Nueva Consulta"
   - Selecciona paciente y doctor
   - Completa los datos de la consulta
   - Guarda

### **Como Doctor:**
1. **Inicia sesión** con tu usuario de doctor
2. **Ve el Dashboard** con tus estadísticas
3. **Busca pacientes** en la sección Pacientes
4. **Crea consultas** para tus pacientes

## 🔧 Comandos Útiles

### **Desarrollo**
```bash
# Verificar el sistema
python manage.py check

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic
```

### **Testing**
```bash
# Ejecutar tests
python manage.py test

# Tests con cobertura
coverage run --source='.' manage.py test
coverage report
```

## 📁 Estructura de Archivos Importantes

```
system-medic/
├── manage.py              # Script principal
├── requirements-dev.txt   # Dependencias de desarrollo
├── .venv/                # Entorno virtual
├── db.sqlite3            # Base de datos
├── static/               # Archivos estáticos
│   ├── css/custom.css    # Estilos personalizados
│   └── js/custom.js      # JavaScript personalizado
└── history/              # Aplicación principal
    ├── models.py         # Modelos de datos
    ├── views.py          # Vistas
    ├── forms.py          # Formularios
    └── templates/        # Plantillas HTML
```

## 🆘 Solución Rápida de Problemas

### **Error: "No module named 'django'"**
```bash
# Solución: Activar entorno virtual
.\.venv\Scripts\activate
```

### **Error: "Database is locked"**
```bash
# Solución: Cerrar el servidor y reiniciar
# Ctrl+C para detener
python manage.py runserver
```

### **Error: "Table doesn't exist"**
```bash
# Solución: Aplicar migraciones
python manage.py migrate
```

### **Error: "Static files not found"**
```bash
# Solución: Recolectar archivos estáticos
python manage.py collectstatic
```

## 📊 Datos de Prueba

### **Crear Datos de Ejemplo**
```bash
# Crear superusuario
python manage.py createsuperuser

# Crear datos de prueba (si existe el comando)
python manage.py loaddata fixtures/sample_data.json
```

### **Datos de Prueba Manuales**
1. **Doctor de Prueba:**
   - Usuario: doctor1
   - Contraseña: doctor123
   - Especialidad: Medicina General

2. **Paciente de Prueba:**
   - Nombre: Juan Pérez
   - DNI: 12345678
   - Email: juan@ejemplo.com

## 🔗 Enlaces Útiles

- **Sistema:** http://127.0.0.1:8000/
- **Admin Django:** http://127.0.0.1:8000/admin/
- **Documentación Técnica:** DOCUMENTACION_TECNICA.md
- **Manual de Usuario:** MANUAL_USUARIO.md

## 📞 Soporte

- **Problemas técnicos:** Revisar DOCUMENTACION_TECNICA.md
- **Uso del sistema:** Revisar MANUAL_USUARIO.md
- **Issues:** Crear issue en el repositorio

---

**¡Listo para usar System Medic!** 🏥✨

