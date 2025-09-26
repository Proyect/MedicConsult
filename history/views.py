from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Person, Doctor, Consult, Diagnosis, Treatment, MedicalRecord
from .forms import (
    PatientForm, DoctorForm, DoctorUserForm, ConsultForm, 
    DiagnosisForm, TreatmentForm, MedicalRecordForm, PatientSearchForm
)
from .utils import (
    is_administrator, is_doctor, get_doctor_profile, 
    can_access_patient, can_access_consult, get_user_role, require_role
)

@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenido, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales inválidas')
    else:
        form = AuthenticationForm()
    
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente')
    return redirect('login')

@login_required
def dashboard(request):
    try:
        user_role = get_user_role(request.user)
        
        # Estadísticas básicas - solo las que sabemos que funcionan
        total_patients = Person.objects.count()
        total_consults = Consult.objects.count()
        
        # Consultas recientes
        recent_consults = Consult.objects.all().order_by('-date')[:5]
        
        context = {
            'user_role': user_role,
            'total_patients': total_patients,
            'total_consults': total_consults,
            'total_doctors': 0,  # Temporalmente en 0
            'consults_this_month': 0,  # Temporalmente en 0
            'recent_consults': recent_consults,
            'consults_by_type': [],  # Temporalmente vacío
            'patients_by_gender': [],  # Temporalmente vacío
        }
        
        return render(request, 'dashboard.html', context)
    except Exception as e:
        print(f"Error en dashboard: {e}")
        # Vista simplificada en caso de error
        return render(request, 'dashboard.html', {
            'user_role': 'administrator',
            'total_patients': 0,
            'total_consults': 0,
            'total_doctors': 0,
            'consults_this_month': 0,
            'recent_consults': [],
            'consults_by_type': [],
            'patients_by_gender': [],
        })

@login_required
def dashboard_data_api(request):
    """API para obtener datos del dashboard"""
    if request.method == 'GET':
        from .reports import get_statistics_data
        data = get_statistics_data()
        return JsonResponse(data)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# ========== PACIENTES ==========

@login_required
@require_role('any')
def patient_list(request):
    search_form = PatientSearchForm(request.GET)
    patients = Person.objects.filter(is_active=True)
    
    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        gender = search_form.cleaned_data.get('gender')
        
        if search:
            patients = patients.filter(
                Q(name__icontains=search) | 
                Q(last_name__icontains=search) | 
                Q(dni__icontains=search)
            )
        
        if gender:
            patients = patients.filter(gender=gender)
    
    # Si es doctor, solo mostrar sus pacientes
    if get_user_role(request.user) == 'doctor':
        doctor = get_doctor_profile(request.user)
        if doctor:
            patient_ids = Consult.objects.filter(doctor=doctor).values_list('patient_id', flat=True)
            patients = patients.filter(id__in=patient_ids)
    
    paginator = Paginator(patients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'patients/list.html', {
        'page_obj': page_obj,
        'search_form': search_form,
        'user_role': get_user_role(request.user)
    })

@login_required
@require_role('any')
def patient_detail(request, pk):
    patient = get_object_or_404(Person, pk=pk, is_active=True)
    
    if not can_access_patient(request.user, patient):
        messages.error(request, 'No tienes permisos para ver este paciente')
        return redirect('patient_list')
    
    consults = Consult.objects.filter(patient=patient).order_by('-date')
    medical_record, created = MedicalRecord.objects.get_or_create(patient=patient)
    
    return render(request, 'patients/detail.html', {
        'patient': patient,
        'consults': consults,
        'medical_record': medical_record,
        'user_role': get_user_role(request.user)
    })

@login_required
@require_role('administrator')
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'Paciente {patient.name} {patient.last_name} creado exitosamente')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm()
    
    return render(request, 'patients/form.html', {
        'form': form,
        'title': 'Nuevo Paciente',
        'user_role': get_user_role(request.user)
    })

@login_required
@require_role('administrator')
def patient_edit(request, pk):
    patient = get_object_or_404(Person, pk=pk, is_active=True)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, f'Paciente {patient.name} {patient.last_name} actualizado exitosamente')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    
    return render(request, 'patients/form.html', {
        'form': form,
        'title': f'Editar {patient.name} {patient.last_name}',
        'patient': patient,
        'user_role': get_user_role(request.user)
    })

@login_required
@require_role('administrator')
def patient_delete(request, pk):
    patient = get_object_or_404(Person, pk=pk, is_active=True)
    
    if request.method == 'POST':
        patient.is_active = False
        patient.save()
        messages.success(request, f'Paciente {patient.name} {patient.last_name} desactivado exitosamente')
        return redirect('patient_list')
    
    return render(request, 'patients/confirm_delete.html', {
        'patient': patient,
        'user_role': get_user_role(request.user)
    })

# ========== CONSULTAS ==========

@login_required
@require_role('any')
def consult_list(request):
    consults = Consult.objects.all().order_by('-date')
    
    # Si es doctor, solo mostrar sus consultas
    if get_user_role(request.user) == 'doctor':
        doctor = get_doctor_profile(request.user)
        if doctor:
            consults = consults.filter(doctor=doctor)
    
    paginator = Paginator(consults, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'consults/list.html', {
        'page_obj': page_obj,
        'user_role': get_user_role(request.user)
    })

@login_required
@require_role('any')
def consult_detail(request, pk):
    consult = get_object_or_404(Consult, pk=pk)
    
    if not can_access_consult(request.user, consult):
        messages.error(request, 'No tienes permisos para ver esta consulta')
        return redirect('consult_list')
    
    try:
        diagnosis = Diagnosis.objects.get(consult=consult)
    except Diagnosis.DoesNotExist:
        diagnosis = None
    
    try:
        treatment = Treatment.objects.get(consult=consult)
    except Treatment.DoesNotExist:
        treatment = None
    
    return render(request, 'consults/detail.html', {
        'consult': consult,
        'diagnosis': diagnosis,
        'treatment': treatment,
        'user_role': get_user_role(request.user)
    })

@login_required
@require_role('any')
def consult_create(request):
    if request.method == 'POST':
        form = ConsultForm(request.POST)
        if form.is_valid():
            consult = form.save()
            messages.success(request, f'Consulta creada exitosamente')
            return redirect('consult_detail', pk=consult.pk)
    else:
        form = ConsultForm()
        # Si es doctor, preseleccionar el doctor actual
        if get_user_role(request.user) == 'doctor':
            doctor = get_doctor_profile(request.user)
            if doctor:
                form.fields['doctor'].initial = doctor
    
    return render(request, 'consults/form.html', {
        'form': form,
        'title': 'Nueva Consulta',
        'user_role': get_user_role(request.user)
    })

# ========== DOCTORES ==========

@login_required
@require_role('administrator')
def doctor_list(request):
    doctors = Doctor.objects.filter(is_active=True)
    paginator = Paginator(doctors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'doctors/list.html', {
        'page_obj': page_obj,
        'user_role': get_user_role(request.user)
    })

@login_required
@require_role('administrator')
def doctor_create(request):
    if request.method == 'POST':
        user_form = DoctorUserForm(request.POST)
        doctor_form = DoctorForm(request.POST)
        
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            messages.success(request, f'Doctor {user.get_full_name()} creado exitosamente')
            return redirect('doctor_list')
    else:
        user_form = DoctorUserForm()
        doctor_form = DoctorForm()
    
    return render(request, 'doctors/form.html', {
        'user_form': user_form,
        'doctor_form': doctor_form,
        'title': 'Nuevo Doctor',
        'user_role': get_user_role(request.user)
    })

# ========== HISTORIA CLÍNICA ==========

@login_required
@require_role('any')
def medical_record_edit(request, patient_pk):
    patient = get_object_or_404(Person, pk=patient_pk, is_active=True)
    
    if not can_access_patient(request.user, patient):
        messages.error(request, 'No tienes permisos para editar esta historia clínica')
        return redirect('patient_list')
    
    medical_record, created = MedicalRecord.objects.get_or_create(patient=patient)
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, instance=medical_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Historia clínica actualizada exitosamente')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = MedicalRecordForm(instance=medical_record)
    
    return render(request, 'medical_record/form.html', {
        'form': form,
        'patient': patient,
        'title': f'Historia Clínica de {patient.name} {patient.last_name}',
        'user_role': get_user_role(request.user)
    })