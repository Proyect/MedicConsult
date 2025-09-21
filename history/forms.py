from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Person, Doctor, Consult, Diagnosis, Treatment, MedicalRecord

class PatientForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'last_name', 'dni', 'birth_date', 'gender', 'phone', 'email', 'address', 'observations']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DNI (solo números)'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dirección completa'}),
            'observations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones adicionales'}),
        }

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['license_number', 'specialty', 'phone']
        widgets = {
            'license_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Matrícula'}),
            'specialty': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
        }

class DoctorUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        }

class ConsultForm(forms.ModelForm):
    class Meta:
        model = Consult
        fields = ['patient', 'doctor', 'date', 'consult_type', 'reason', 'symptoms', 'vital_signs']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'consult_type': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Motivo de la consulta'}),
            'symptoms': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Síntomas presentados'}),
            'vital_signs': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Signos vitales (presión, temperatura, etc.)'}),
        }

class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['description', 'icd_code']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción detallada del diagnóstico'}),
            'icd_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código ICD-10 (opcional)'}),
        }

class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ['description', 'medications', 'instructions', 'follow_up_date']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción del tratamiento'}),
            'medications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Medicamentos recetados'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Instrucciones para el paciente'}),
            'follow_up_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['allergies', 'chronic_conditions', 'family_history', 'social_history']
        widgets = {
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Alergias conocidas'}),
            'chronic_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enfermedades crónicas'}),
            'family_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Antecedentes familiares'}),
            'social_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Antecedentes sociales'}),
        }

class PatientSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre, apellido o DNI...'
        })
    )
    gender = forms.ChoiceField(
        choices=[('', 'Todos')] + Person.GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

