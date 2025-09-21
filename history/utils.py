from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .models import Doctor

def is_administrator(user):
    """Verifica si el usuario es administrador"""
    return user.is_superuser or user.is_staff

def is_doctor(user):
    """Verifica si el usuario es doctor"""
    try:
        return Doctor.objects.filter(user=user, is_active=True).exists()
    except:
        return False

def get_doctor_profile(user):
    """Obtiene el perfil de doctor del usuario"""
    try:
        return Doctor.objects.get(user=user, is_active=True)
    except Doctor.DoesNotExist:
        return None

def can_access_patient(user, patient):
    """
    Verifica si el usuario puede acceder a los datos de un paciente específico
    - Los administradores pueden acceder a todos los pacientes
    - Los doctores solo pueden acceder a sus propios pacientes (con consultas)
    """
    if is_administrator(user):
        return True
    
    if is_doctor(user):
        doctor = get_doctor_profile(user)
        if doctor:
            # Verificar si el doctor tiene consultas con este paciente
            return Consult.objects.filter(doctor=doctor, patient=patient).exists()
    
    return False

def can_access_consult(user, consult):
    """
    Verifica si el usuario puede acceder a una consulta específica
    - Los administradores pueden acceder a todas las consultas
    - Los doctores solo pueden acceder a sus propias consultas
    """
    if is_administrator(user):
        return True
    
    if is_doctor(user):
        doctor = get_doctor_profile(user)
        if doctor:
            return consult.doctor == doctor
    
    return False

def get_user_role(user):
    """Retorna el rol del usuario"""
    if is_administrator(user):
        return 'administrator'
    elif is_doctor(user):
        return 'doctor'
    else:
        return 'none'

def require_role(required_role):
    """
    Decorator para requerir un rol específico
    Uso: @require_role('administrator') o @require_role('doctor')
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user_role = get_user_role(request.user)
            
            if required_role == 'administrator' and not is_administrator(request.user):
                raise PermissionDenied("Se requieren permisos de administrador")
            elif required_role == 'doctor' and not is_doctor(request.user):
                raise PermissionDenied("Se requieren permisos de doctor")
            elif required_role == 'any' and user_role == 'none':
                raise PermissionDenied("Se requiere autenticación")
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

