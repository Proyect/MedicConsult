from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone

class Person(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellido")
    dni = models.CharField(
        max_length=20, 
        unique=True, 
        validators=[RegexValidator(
            regex=r'^\d{7,8}$',
            message='El DNI debe contener entre 7 y 8 dígitos'
        )],
        verbose_name="DNI"
    )
    birth_date = models.DateField(verbose_name="Fecha de Nacimiento")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Género")
    phone = models.CharField(
        max_length=15, 
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message='Formato de teléfono inválido'
        )],
        verbose_name="Teléfono"
    )
    email = models.EmailField(unique=True, verbose_name="Email")
    address = models.TextField(verbose_name="Dirección")
    observations = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['last_name', 'name']

    def __str__(self) -> str:
        return f"{self.name} {self.last_name} - DNI: {self.dni}"
    
    @property
    def age(self):
        today = timezone.now().date()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

class Doctor(models.Model):
    SPECIALTY_CHOICES = [
        ('GP', 'Medicina General'),
        ('CARD', 'Cardiología'),
        ('DERM', 'Dermatología'),
        ('NEURO', 'Neurología'),
        ('PED', 'Pediatría'),
        ('GYN', 'Ginecología'),
        ('ORTH', 'Ortopedia'),
        ('PSYCH', 'Psiquiatría'),
        ('OTHER', 'Otra'),
    ]
    
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    license_number = models.CharField(max_length=20, unique=True, verbose_name="Número de Matrícula")
    specialty = models.CharField(max_length=10, choices=SPECIALTY_CHOICES, verbose_name="Especialidad")
    phone = models.CharField(
        max_length=15, 
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message='Formato de teléfono inválido'
        )],
        verbose_name="Teléfono"
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctores"
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self) -> str:
        return f"Dr. {self.user.get_full_name()} - {self.get_specialty_display()}"
    
    @property
    def full_name(self):
        return self.user.get_full_name()

class Consult(models.Model):
    CONSULT_TYPE_CHOICES = [
        ('FIRST', 'Primera Consulta'),
        ('FOLLOW', 'Consulta de Seguimiento'),
        ('EMERGENCY', 'Emergencia'),
        ('ROUTINE', 'Consulta de Rutina'),
    ]
    
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Paciente")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Doctor")
    date = models.DateTimeField(verbose_name="Fecha y Hora")
    consult_type = models.CharField(max_length=10, choices=CONSULT_TYPE_CHOICES, verbose_name="Tipo de Consulta")
    reason = models.TextField(verbose_name="Motivo de Consulta")
    symptoms = models.TextField(verbose_name="Síntomas")
    vital_signs = models.TextField(blank=True, null=True, verbose_name="Signos Vitales")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        ordering = ['-date']

    def __str__(self) -> str:
        return f"Consulta {self.id} - {self.patient} con Dr. {self.doctor.full_name} - {self.date.strftime('%d/%m/%Y %H:%M')}"

class Diagnosis(models.Model):
    id = models.AutoField(primary_key=True)
    consult = models.OneToOneField(Consult, on_delete=models.CASCADE, verbose_name="Consulta")
    description = models.TextField(verbose_name="Descripción del Diagnóstico")
    icd_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Código ICD-10")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Diagnóstico"
        verbose_name_plural = "Diagnósticos"

    def __str__(self) -> str:
        return f"Diagnóstico para consulta {self.consult.id}"

class Treatment(models.Model):
    id = models.AutoField(primary_key=True)
    consult = models.OneToOneField(Consult, on_delete=models.CASCADE, verbose_name="Consulta")
    description = models.TextField(verbose_name="Descripción del Tratamiento")
    medications = models.TextField(blank=True, null=True, verbose_name="Medicamentos")
    instructions = models.TextField(blank=True, null=True, verbose_name="Instrucciones")
    follow_up_date = models.DateField(blank=True, null=True, verbose_name="Fecha de Seguimiento")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tratamiento"
        verbose_name_plural = "Tratamientos"

    def __str__(self) -> str:
        return f"Tratamiento para consulta {self.consult.id}"

class MedicalRecord(models.Model):
    """Historia clínica completa del paciente"""
    id = models.AutoField(primary_key=True)
    patient = models.OneToOneField(Person, on_delete=models.CASCADE, verbose_name="Paciente")
    allergies = models.TextField(blank=True, null=True, verbose_name="Alergias")
    chronic_conditions = models.TextField(blank=True, null=True, verbose_name="Enfermedades Crónicas")
    family_history = models.TextField(blank=True, null=True, verbose_name="Antecedentes Familiares")
    social_history = models.TextField(blank=True, null=True, verbose_name="Antecedentes Sociales")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Historia Clínica"
        verbose_name_plural = "Historias Clínicas"

    def __str__(self) -> str:
        return f"Historia Clínica de {self.patient}"
    
