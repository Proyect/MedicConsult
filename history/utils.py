from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect
from .models import Doctor, UserProfile, Consult

def is_administrator(user):
    """Verifica si el usuario es administrador"""
    if not user or not hasattr(user, 'is_superuser'):
        return False
    return user.is_superuser or user.is_staff

def is_doctor(user):
    """Verifica si el usuario es doctor"""
    if not user or not hasattr(user, 'is_authenticated') or not user.is_authenticated:
        return False
    try:
        return Doctor.objects.filter(user=user, is_active=True).exists()
    except:
        return False

def get_doctor_profile(user):
    """Obtiene el perfil de doctor del usuario"""
    if not user or not hasattr(user, 'is_authenticated') or not user.is_authenticated:
        return None
    try:
        return Doctor.objects.get(user=user, is_active=True)
    except Doctor.DoesNotExist:
        return None
    except:
        return None

def can_access_patient(user, patient):
    """
    Verifica si el usuario puede acceder a los datos de un paciente específico
    - Los administradores pueden acceder a todos los pacientes
    - Los doctores solo pueden acceder a sus propios pacientes (con consultas)
    """
    if not user or not patient:
        return False
        
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
    if not user or not consult:
        return False
        
    if is_administrator(user):
        return True
    
    if is_doctor(user):
        doctor = get_doctor_profile(user)
        if doctor:
            return consult.doctor == doctor
    
    return False

def is_patient(user):
    """Verificar si el usuario es paciente"""
    try:
        profile = UserProfile.objects.get(user=user)
        return profile.role == 'PATIENT'
    except UserProfile.DoesNotExist:
        return False

def get_user_profile(user):
    """Obtener el perfil extendido del usuario"""
    try:
        return UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        # Crear perfil por defecto si no existe
        return UserProfile.objects.create(
            user=user,
            role='PATIENT',
            phone=''
        )

def get_user_role(user):
    """Retorna el rol del usuario"""
    if is_administrator(user):
        return 'administrator'
    elif is_doctor(user):
        return 'doctor'
    elif is_patient(user):
        return 'patient'
    else:
        # Si no tiene perfil, crear uno por defecto
        try:
            profile = get_user_profile(user)
            return profile.role.lower()
        except:
            return 'patient'

def require_role(required_role):
    """
    Decorator para requerir un rol específico
    Uso: @require_role('administrator'), @require_role('doctor'), @require_role('patient'), @require_role('any')
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user_role = get_user_role(request.user)
            
            if required_role == 'any':
                return view_func(request, *args, **kwargs)
            elif required_role == 'administrator' and user_role == 'administrator':
                return view_func(request, *args, **kwargs)
            elif required_role == 'doctor' and user_role in ['administrator', 'doctor']:
                return view_func(request, *args, **kwargs)
            elif required_role == 'patient' and user_role in ['administrator', 'doctor', 'patient']:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'No tienes permisos para acceder a esta página')
                return redirect('dashboard')
        
        return wrapper
    return decorator

def log_audit_action(user, action, model_name, object_id=None, description="", request=None):
    """Registrar acción en el log de auditoría"""
    from .models import AuditLog
    
    AuditLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=str(object_id) if object_id else None,
        description=description,
        ip_address=request.META.get('REMOTE_ADDR') if request else None,
        user_agent=request.META.get('HTTP_USER_AGENT') if request else None
    )

