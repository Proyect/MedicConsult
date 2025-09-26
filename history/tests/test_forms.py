import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from history.forms import (
    PatientForm, DoctorForm, DoctorUserForm, ConsultForm, 
    DiagnosisForm, TreatmentForm, MedicalRecordForm, PatientSearchForm
)
from history.models import Person, Doctor, Consult, Diagnosis, Treatment, MedicalRecord
from datetime import date, datetime


class PatientFormTest(TestCase):
    """Tests para el formulario de pacientes"""
    
    def test_patient_form_valid_data(self):
        """Test formulario con datos válidos"""
        form_data = {
            'name': 'Juan',
            'last_name': 'Pérez',
            'dni': '12345678',
            'birth_date': '1990-01-01',
            'gender': 'M',
            'phone': '+54911234567',
            'email': 'juan.perez@example.com',
            'address': 'Calle 123, Ciudad',
            'observations': 'Paciente regular'
        }
        form = PatientForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_patient_form_invalid_dni(self):
        """Test formulario con DNI inválido"""
        form_data = {
            'name': 'Juan',
            'last_name': 'Pérez',
            'dni': '123',  # DNI muy corto
            'birth_date': '1990-01-01',
            'gender': 'M',
            'phone': '+54911234567',
            'email': 'juan.perez@example.com',
            'address': 'Calle 123, Ciudad'
        }
        form = PatientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('dni', form.errors)
    
    def test_patient_form_dni_with_letters(self):
        """Test formulario con DNI que contiene letras"""
        form_data = {
            'name': 'Juan',
            'last_name': 'Pérez',
            'dni': '1234567a',  # DNI con letra
            'birth_date': '1990-01-01',
            'gender': 'M',
            'phone': '+54911234567',
            'email': 'juan.perez@example.com',
            'address': 'Calle 123, Ciudad'
        }
        form = PatientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('dni', form.errors)
    
    def test_patient_form_invalid_phone(self):
        """Test formulario con teléfono inválido"""
        form_data = {
            'name': 'Juan',
            'last_name': 'Pérez',
            'dni': '12345678',
            'birth_date': '1990-01-01',
            'gender': 'M',
            'phone': '123',  # Teléfono muy corto
            'email': 'juan.perez@example.com',
            'address': 'Calle 123, Ciudad'
        }
        form = PatientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
    
    def test_patient_form_future_birth_date(self):
        """Test formulario con fecha de nacimiento futura"""
        form_data = {
            'name': 'Juan',
            'last_name': 'Pérez',
            'dni': '12345678',
            'birth_date': '2030-01-01',  # Fecha futura
            'gender': 'M',
            'phone': '+54911234567',
            'email': 'juan.perez@example.com',
            'address': 'Calle 123, Ciudad'
        }
        form = PatientForm(data=form_data)
        # Como las validaciones fueron removidas, el formulario será válido
        self.assertTrue(form.is_valid())
    
    def test_patient_form_very_old_birth_date(self):
        """Test formulario con fecha de nacimiento muy antigua"""
        form_data = {
            'name': 'Juan',
            'last_name': 'Pérez',
            'dni': '12345678',
            'birth_date': '1800-01-01',  # Fecha muy antigua
            'gender': 'M',
            'phone': '+54911234567',
            'email': 'juan.perez@example.com',
            'address': 'Calle 123, Ciudad'
        }
        form = PatientForm(data=form_data)
        # Como las validaciones fueron removidas, el formulario será válido
        self.assertTrue(form.is_valid())
    
    def test_patient_form_missing_required_fields(self):
        """Test formulario con campos requeridos faltantes"""
        form_data = {
            'name': 'Juan',
            # Faltan campos requeridos
        }
        form = PatientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)
        self.assertIn('dni', form.errors)
        self.assertIn('birth_date', form.errors)
        self.assertIn('gender', form.errors)
        self.assertIn('phone', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('address', form.errors)


class DoctorFormTest(TestCase):
    """Tests para el formulario de doctores"""
    
    def test_doctor_form_valid_data(self):
        """Test formulario con datos válidos"""
        form_data = {
            'license_number': 'MP12345',
            'specialty': 'GP',
            'phone': '+54911234567'
        }
        form = DoctorForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_doctor_form_missing_required_fields(self):
        """Test formulario con campos requeridos faltantes"""
        form_data = {
            'license_number': 'MP12345',
            # Faltan specialty y phone
        }
        form = DoctorForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('specialty', form.errors)
        self.assertIn('phone', form.errors)


class DoctorUserFormTest(TestCase):
    """Tests para el formulario de usuario de doctor"""
    
    def test_doctor_user_form_valid_data(self):
        """Test formulario con datos válidos"""
        form_data = {
            'username': 'doctor1',
            'first_name': 'Dr. Juan',
            'last_name': 'Médico',
            'email': 'doctor@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = DoctorUserForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_doctor_user_form_password_mismatch(self):
        """Test formulario con contraseñas que no coinciden"""
        form_data = {
            'username': 'doctor1',
            'first_name': 'Dr. Juan',
            'last_name': 'Médico',
            'email': 'doctor@example.com',
            'password1': 'testpass123',
            'password2': 'differentpass'
        }
        form = DoctorUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_doctor_user_form_missing_required_fields(self):
        """Test formulario con campos requeridos faltantes"""
        form_data = {
            'username': 'doctor1',
            # Faltan campos requeridos
        }
        form = DoctorUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)


class ConsultFormTest(TestCase):
    """Tests para el formulario de consultas"""
    
    def setUp(self):
        # Crear usuario y doctor
        self.user = User.objects.create_user(
            username='doctor1',
            email='doctor@example.com',
            password='testpass123',
            first_name='Dr. Juan',
            last_name='Médico'
        )
        self.doctor = Doctor.objects.create(
            user=self.user,
            license_number='MP12345',
            specialty='GP',
            phone='+54911234567'
        )
        
        # Crear paciente
        self.patient = Person.objects.create(
            name='Juan',
            last_name='Pérez',
            dni='12345678',
            birth_date=date(1990, 1, 1),
            gender='M',
            phone='+54911234567',
            email='juan.perez@example.com',
            address='Calle 123, Ciudad'
        )
    
    def test_consult_form_valid_data(self):
        """Test formulario con datos válidos"""
        form_data = {
            'patient': self.patient.pk,
            'doctor': self.doctor.pk,
            'date': datetime.now().strftime('%Y-%m-%dT%H:%M'),
            'consult_type': 'FIRST',
            'reason': 'Dolor de cabeza',
            'symptoms': 'Cefalea intensa',
            'vital_signs': 'TA: 120/80'
        }
        form = ConsultForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_consult_form_missing_required_fields(self):
        """Test formulario con campos requeridos faltantes"""
        form_data = {
            'patient': self.patient.pk,
            'doctor': self.doctor.pk,
            # Faltan campos requeridos
        }
        form = ConsultForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        self.assertIn('consult_type', form.errors)
        self.assertIn('reason', form.errors)
        self.assertIn('symptoms', form.errors)


class DiagnosisFormTest(TestCase):
    """Tests para el formulario de diagnósticos"""
    
    def test_diagnosis_form_valid_data(self):
        """Test formulario con datos válidos"""
        form_data = {
            'description': 'Migraña tensional',
            'icd_code': 'G44.2'
        }
        form = DiagnosisForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_diagnosis_form_missing_required_fields(self):
        """Test formulario con campos requeridos faltantes"""
        form_data = {
            'icd_code': 'G44.2'
            # Falta description
        }
        form = DiagnosisForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)


class TreatmentFormTest(TestCase):
    """Tests para el formulario de tratamientos"""
    
    def test_treatment_form_valid_data(self):
        """Test formulario con datos válidos"""
        form_data = {
            'description': 'Reposo y medicación',
            'medications': 'Ibuprofeno 400mg cada 8 horas',
            'instructions': 'Tomar con comida',
            'follow_up_date': '2024-02-01'
        }
        form = TreatmentForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_treatment_form_missing_required_fields(self):
        """Test formulario con campos requeridos faltantes"""
        form_data = {
            'medications': 'Ibuprofeno 400mg cada 8 horas'
            # Falta description
        }
        form = TreatmentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)


class MedicalRecordFormTest(TestCase):
    """Tests para el formulario de historia clínica"""
    
    def test_medical_record_form_valid_data(self):
        """Test formulario con datos válidos"""
        form_data = {
            'allergies': 'Penicilina',
            'chronic_conditions': 'Diabetes tipo 2',
            'family_history': 'Hipertensión en familia paterna',
            'social_history': 'No fuma, no bebe alcohol'
        }
        form = MedicalRecordForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_medical_record_form_empty_data(self):
        """Test formulario con datos vacíos (válido)"""
        form_data = {}
        form = MedicalRecordForm(data=form_data)
        self.assertTrue(form.is_valid())  # Todos los campos son opcionales


class PatientSearchFormTest(TestCase):
    """Tests para el formulario de búsqueda de pacientes"""
    
    def test_patient_search_form_valid_data(self):
        """Test formulario con datos válidos"""
        form_data = {
            'search': 'Juan',
            'gender': 'M'
        }
        form = PatientSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_patient_search_form_empty_data(self):
        """Test formulario con datos vacíos (válido)"""
        form_data = {}
        form = PatientSearchForm(data=form_data)
        self.assertTrue(form.is_valid())  # Todos los campos son opcionales
    
    def test_patient_search_form_invalid_gender(self):
        """Test formulario con género inválido"""
        form_data = {
            'search': 'Juan',
            'gender': 'X'  # Género inválido
        }
        form = PatientSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('gender', form.errors)

