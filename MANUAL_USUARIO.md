# 👥 Manual del Usuario - System Medic

## 🏥 Bienvenido a System Medic

**System Medic** es un sistema integral de gestión para consultorios médicos que te permite administrar pacientes, consultas, doctores e historias clínicas de manera eficiente y segura.

## 🚀 Acceso al Sistema

### **Primer Acceso**
1. Abre tu navegador web
2. Ve a la dirección: `http://127.0.0.1:8000/`
3. Usa las credenciales proporcionadas:
   - **Usuario:** admin
   - **Contraseña:** admin123

### **Cambiar Contraseña**
1. Haz clic en tu nombre de usuario (esquina superior derecha)
2. Selecciona "Administración"
3. Ve a "Usuarios" → "Usuarios"
4. Busca tu usuario y haz clic en "Cambiar contraseña"

## 🏠 Dashboard Principal

### **¿Qué puedes ver en el Dashboard?**

#### **📊 Estadísticas Generales**
- **Pacientes Activos:** Número total de pacientes registrados
- **Total Consultas:** Cantidad de consultas realizadas
- **Doctores Activos:** Número de doctores en el sistema
- **Mis Consultas:** (Solo para doctores) Tus consultas realizadas

#### **⚡ Acciones Rápidas**
- **Nuevo Paciente:** Registrar un nuevo paciente
- **Nueva Consulta:** Crear una consulta médica
- **Buscar Paciente:** Encontrar pacientes existentes
- **Nuevo Doctor:** (Solo administradores) Registrar un nuevo doctor

#### **📋 Consultas Recientes** (Solo para Doctores)
- Lista de tus últimas 5 consultas
- Información rápida del paciente y tipo de consulta
- Acceso directo para ver detalles

## 👤 Gestión de Pacientes

### **Ver Lista de Pacientes**
1. En el menú principal, haz clic en "Pacientes"
2. Verás una tabla con todos los pacientes
3. Usa los filtros para buscar por:
   - **Nombre o Apellido**
   - **DNI**
   - **Género**

### **Agregar Nuevo Paciente**
1. Haz clic en "Nuevo Paciente" (botón azul)
2. Completa el formulario:
   - **Nombre:** Nombre del paciente
   - **Apellido:** Apellido del paciente
   - **DNI:** Solo números (7-8 dígitos)
   - **Fecha de Nacimiento:** Se calculará la edad automáticamente
   - **Género:** Masculino, Femenino u Otro
   - **Teléfono:** Se formateará automáticamente
   - **Email:** Debe ser único
   - **Dirección:** Dirección completa
   - **Observaciones:** Información adicional
3. Haz clic en "Guardar"

### **Ver Detalles de un Paciente**
1. En la lista de pacientes, haz clic en el ícono del ojo 👁️
2. Verás:
   - **Información Personal:** Datos básicos del paciente
   - **Historia Clínica:** Alergias, enfermedades crónicas, antecedentes
   - **Consultas:** Lista de todas las consultas realizadas
   - **Acciones:** Editar, ver historia clínica, etc.

### **Editar Paciente**
1. En la lista de pacientes, haz clic en el ícono del lápiz ✏️
2. Modifica los datos necesarios
3. Haz clic en "Guardar"

### **Desactivar Paciente**
1. En la lista de pacientes, haz clic en el ícono de la papelera 🗑️
2. Confirma la acción
3. El paciente se desactivará (no se eliminará)

## 🩺 Gestión de Consultas

### **Ver Lista de Consultas**
1. En el menú principal, haz clic en "Consultas"
2. Verás todas las consultas ordenadas por fecha (más recientes primero)
3. Los doctores solo ven sus propias consultas

### **Crear Nueva Consulta**
1. Haz clic en "Nueva Consulta" (botón verde)
2. Completa el formulario:
   - **Paciente:** Selecciona de la lista
   - **Doctor:** Se preselecciona si eres doctor
   - **Fecha y Hora:** Cuándo se realizó la consulta
   - **Tipo de Consulta:**
     - 🔵 **Primera Consulta:** Primera vez del paciente
     - 🟢 **Consulta de Seguimiento:** Control de seguimiento
     - 🔴 **Emergencia:** Urgencia médica
     - 🟠 **Consulta de Rutina:** Control de rutina
   - **Motivo de Consulta:** Por qué viene el paciente
   - **Síntomas:** Qué síntomas presenta
   - **Signos Vitales:** Presión, temperatura, etc.
3. Haz clic en "Guardar"

### **Ver Detalles de una Consulta**
1. En la lista de consultas, haz clic en "Ver"
2. Verás:
   - **Información de la Consulta:** Datos básicos
   - **Diagnóstico:** Si existe
   - **Tratamiento:** Si existe
   - **Acciones:** Agregar diagnóstico/tratamiento

### **Agregar Diagnóstico**
1. En los detalles de la consulta, haz clic en "Agregar Diagnóstico"
2. Completa:
   - **Descripción:** Diagnóstico detallado
   - **Código ICD-10:** (Opcional) Código internacional
3. Haz clic en "Guardar"

### **Agregar Tratamiento**
1. En los detalles de la consulta, haz clic en "Agregar Tratamiento"
2. Completa:
   - **Descripción:** Tratamiento prescrito
   - **Medicamentos:** Medicamentos recetados
   - **Instrucciones:** Instrucciones para el paciente
   - **Fecha de Seguimiento:** Cuándo volver
3. Haz clic en "Guardar"

## 👨‍⚕️ Gestión de Doctores (Solo Administradores)

### **Ver Lista de Doctores**
1. En el menú principal, haz clic en "Doctores"
2. Verás todos los doctores registrados

### **Agregar Nuevo Doctor**
1. Haz clic en "Nuevo Doctor" (botón naranja)
2. Completa el formulario de usuario:
   - **Nombre de Usuario:** Para iniciar sesión
   - **Nombre:** Nombre del doctor
   - **Apellido:** Apellido del doctor
   - **Email:** Email del doctor
   - **Contraseña:** Contraseña segura
3. Completa el formulario de doctor:
   - **Número de Matrícula:** Número único de matrícula
   - **Especialidad:** Selecciona la especialidad médica
   - **Teléfono:** Teléfono de contacto
4. Haz clic en "Guardar"

## 📋 Historia Clínica

### **Editar Historia Clínica**
1. En los detalles de un paciente, haz clic en "Historia Clínica"
2. Completa las secciones:
   - **Alergias:** Alergias conocidas del paciente
   - **Enfermedades Crónicas:** Condiciones crónicas
   - **Antecedentes Familiares:** Historia familiar médica
   - **Antecedentes Sociales:** Hábitos, trabajo, etc.
3. Haz clic en "Guardar"

## 🔍 Búsqueda y Filtros

### **Buscar Pacientes**
1. En la página de pacientes, usa el campo de búsqueda
2. Puedes buscar por:
   - **Nombre completo**
   - **Apellido**
   - **DNI**
3. Usa el filtro de género para refinar resultados

### **Navegación por Páginas**
- Si hay muchos resultados, usa la paginación en la parte inferior
- Navega entre páginas con los botones de flecha
- Ve directamente a la primera o última página

## 🎨 Características del Diseño

### **Colores y Símbolos**
- 🔵 **Azul:** Primera consulta, información general
- 🟢 **Verde:** Seguimiento, éxito, confirmación
- 🔴 **Rojo:** Emergencia, error, advertencia
- 🟠 **Naranja:** Rutina, advertencia
- ⚪ **Gris:** Información secundaria

### **Iconos Utilizados**
- 👤 **Persona:** Usuarios, pacientes
- 🏥 **Hospital:** Sistema médico
- 📋 **Clipboard:** Consultas, formularios
- 👨‍⚕️ **Doctor:** Personal médico
- 🔍 **Lupa:** Búsqueda
- ✏️ **Lápiz:** Editar
- 🗑️ **Papelera:** Eliminar
- 👁️ **Ojo:** Ver detalles

## ⌨️ Atajos de Teclado

### **Navegación Rápida**
- **Ctrl + N:** Nuevo elemento (en páginas de lista)
- **Escape:** Cerrar modales y alertas
- **Enter:** Enviar formularios

### **Formularios**
- **Tab:** Siguiente campo
- **Shift + Tab:** Campo anterior
- **Ctrl + S:** Guardar formulario

## 🔒 Seguridad y Privacidad

### **Control de Acceso**
- **Administradores:** Acceso completo al sistema
- **Doctores:** Solo pueden ver sus pacientes y consultas
- **Sesiones:** Se cierran automáticamente por seguridad

### **Protección de Datos**
- Todos los datos están encriptados
- Acceso solo con autenticación
- Logs de todas las acciones importantes
- Respaldos automáticos de la información

## 🆘 Solución de Problemas

### **No puedo iniciar sesión**
1. Verifica que el usuario y contraseña sean correctos
2. Asegúrate de que las mayúsculas y minúsculas coincidan
3. Contacta al administrador si el problema persiste

### **No veo algunos pacientes/consultas**
- Si eres doctor, solo puedes ver tus propios pacientes
- Los administradores ven todo el sistema
- Verifica que tengas los permisos correctos

### **Error al guardar formularios**
1. Verifica que todos los campos obligatorios estén completos
2. Revisa que los formatos sean correctos (DNI solo números, email válido)
3. Intenta recargar la página y volver a intentar

### **La página se ve rara**
1. Actualiza la página (F5)
2. Verifica tu conexión a internet
3. Contacta al soporte técnico

## 📱 Uso en Móviles

### **Diseño Responsivo**
- El sistema se adapta automáticamente a pantallas pequeñas
- Los menús se colapsan en dispositivos móviles
- Las tablas se pueden desplazar horizontalmente

### **Recomendaciones para Móviles**
- Usa la orientación horizontal para mejor visualización
- Mantén el navegador actualizado
- Usa WiFi cuando sea posible para mejor rendimiento

## 📞 Soporte y Ayuda

### **¿Necesitas Ayuda?**
- **Manual Técnico:** Consulta la documentación técnica
- **Administrador:** Contacta al administrador del sistema
- **Soporte:** [email de soporte]

### **Reportar Problemas**
1. Anota exactamente qué estabas haciendo
2. Toma una captura de pantalla del error
3. Contacta al soporte con esta información

## 🔄 Actualizaciones del Sistema

### **Nuevas Funcionalidades**
- El sistema se actualiza regularmente
- Las nuevas funciones se anuncian en el dashboard
- Consulta este manual para las últimas características

### **Mantenimiento**
- El sistema puede estar temporalmente fuera de servicio para mantenimiento
- Se notifica con anticipación cuando sea posible
- Los datos están seguros durante el mantenimiento

## 📊 Consejos de Uso Eficiente

### **Para Administradores**
- Crea doctores con especialidades específicas
- Mantén actualizada la información de los pacientes
- Revisa regularmente las estadísticas del dashboard
- Haz respaldos periódicos de la información

### **Para Doctores**
- Completa siempre los diagnósticos y tratamientos
- Mantén actualizada la historia clínica de tus pacientes
- Usa los filtros de búsqueda para encontrar pacientes rápidamente
- Revisa las consultas recientes en el dashboard

### **Mejores Prácticas**
- **Siempre verifica** la información antes de guardar
- **Usa descripciones claras** en diagnósticos y tratamientos
- **Mantén actualizada** la información de contacto
- **Guarda frecuentemente** tu trabajo

---

## 🎯 Resumen de Funcionalidades

### **✅ Lo que puedes hacer:**
- 👥 Gestionar pacientes completos
- 🩺 Crear y administrar consultas médicas
- 👨‍⚕️ Administrar doctores y especialidades
- 📋 Mantener historias clínicas detalladas
- 🔍 Buscar y filtrar información
- 📊 Ver estadísticas y reportes
- 🔒 Control de acceso por roles
- 📱 Usar en dispositivos móviles

### **🎨 Características especiales:**
- Diseño médico profesional
- Validación automática de datos
- Formateo inteligente de campos
- Navegación intuitiva
- Seguridad robusta
- Responsive design

---

**¡Bienvenido a System Medic!** 🏥

Este sistema está diseñado para hacer tu trabajo más eficiente y organizado. Si tienes alguna pregunta, no dudes en consultar este manual o contactar al soporte técnico.

**¡Que tengas una excelente experiencia usando System Medic!** ✨

