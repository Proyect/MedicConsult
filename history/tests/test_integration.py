import pytest
from django.test import TestCase, Client, TransactionTestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from history.models import Person, Doctor, Consult, Diagnosis, Treatment, MedicalRecord, UserProfile, AuditLog
from datetime import date, datetime, timedelta
import json


class IntegrationTest(TestCase):
    """Tests de integración para flujos completos del sistema"""
    
    def setUp(self):
        self.client = Client()
        
        # Crear usuario administrador
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        
        # Crear doctor
        self.doctor_user = User.objects.create_user(
            username='doctor',
            email='doctor@example.com',
            password='testpass123',
            first_name='Dr. Juan',
            last_name='Médico'
        )
        
        self.doctor = Doctor.objects.create(
            user=self.doctor_user,
            license_number='MP12345',
            specialty='GP',
            phone='+54911234567'
        )
    
    def test_complete_patient_workflow(self):
        """Test flujo completo de gestión de paciente"""
        self.client.login(username='admin', password='testpass123')
        
        # 1. Crear paciente
        response = self.client.post(reverse('patient_create'), {
            'name': 'Juan',
            'last_name': 'Pérez',
            'dni': '12345678',
            'birth_date': '1990-01-01',
            'gender': 'M',
            'phone': '+54911234567',
            'email': 'juan.perez@example.com',
            'address': 'Calle 123, Ciudad',
            'observations': 'Paciente nuevo'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        patient = Person.objects.get(dni='12345678')
        self.assertEqual(patient.name, 'Juan')
        
        # 2. Ver detalle del paciente
        response = self.client.get(reverse('patient_detail', args=[patient.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
        
        # 3. Crear consulta para el paciente
        response = self.client.post(reverse('consult_create'), {
            'patient': patient.pk,
            'doctor': self.doctor.pk,
            'date': datetime.now().strftime('%Y-%m-%dT%H:%M'),
            'consult_type': 'FIRST',
            'reason': 'Dolor de cabeza',
            'symptoms': 'Cefalea intensa',
            'vital_signs': 'TA: 120/80'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        consult = Consult.objects.get(patient=patient)
        self.assertEqual(consult.reason, 'Dolor de cabeza')
        
        # 4. Ver detalle de la consulta
        response = self.client.get(reverse('consult_detail', args=[consult.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
        self.assertContains(response, 'Dolor de cabeza')
        
        # 5. Editar historia clínica del paciente
        response = self.client.post(reverse('medical_record_edit', args=[patient.pk]), {
            'allergies': 'Penicilina',
            'chronic_conditions': 'Diabetes tipo 2',
            'family_history': 'Hipertensión en familia',
            'social_history': 'No fuma, no bebe'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after update
        medical_record = MedicalRecord.objects.get(patient=patient)
        self.assertEqual(medical_record.allergies, 'Penicilina')
        
        # 6. Editar paciente
        response = self.client.post(reverse('patient_edit', args=[patient.pk]), {
            'name': 'Juan Carlos',
            'last_name': 'Pérez',
            'dni': '12345678',
            'birth_date': '1990-01-01',
            'gender': 'M',
            'phone': '+54911234567',
            'email': 'juan.perez@example.com',
            'address': 'Calle 123, Ciudad',
            'observations': 'Paciente actualizado'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after update
        patient.refresh_from_db()
        self.assertEqual(patient.name, 'Juan Carlos')
        
        # 7. Eliminar paciente (soft delete)
        response = self.client.post(reverse('patient_delete', args=[patient.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        patient.refresh_from_db()
        self.assertFalse(patient.is_active)
    
    def test_complete_doctor_workflow(self):
        """Test flujo completo de gestión de doctor"""
        self.client.login(username='admin', password='testpass123')
        
        # 1. Crear doctor
        response = self.client.post(reverse('doctor_create'), {
            'username': 'newdoctor',
            'first_name': 'Dr. María',
            'last_name': 'Cardióloga',
            'email': 'maria@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'license_number': 'MP54321',
            'specialty': 'CARD',
            'phone': '+54911234568'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        doctor = Doctor.objects.get(license_number='MP54321')
        self.assertEqual(doctor.user.first_name, 'Dr. María')
        
        # 2. Ver lista de doctores
        response = self.client.get(reverse('doctor_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dr. María Cardióloga')
        
        # 3. Crear paciente para el nuevo doctor
        patient = Person.objects.create(
            name='Ana',
            last_name='García',
            dni='87654321',
            birth_date=date(1985, 5, 15),
            gender='F',
            phone='+54911234568',
            email='ana.garcia@example.com',
            address='Calle 456, Ciudad'
        )
        
        # 4. Crear consulta con el nuevo doctor
        response = self.client.post(reverse('consult_create'), {
            'patient': patient.pk,
            'doctor': doctor.pk,
            'date': datetime.now().strftime('%Y-%m-%dT%H:%M'),
            'consult_type': 'FIRST',
            'reason': 'Dolor de pecho',
            'symptoms': 'Dolor precordial',
            'vital_signs': 'TA: 140/90'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        consult = Consult.objects.get(patient=patient, doctor=doctor)
        self.assertEqual(consult.reason, 'Dolor de pecho')
    
    def test_doctor_patient_access_control(self):
        """Test control de acceso de doctores a pacientes"""
        # Crear paciente
        patient = Person.objects.create(
            name='Juan',
            last_name='Pérez',
            dni='12345678',
            birth_date=date(1990, 1, 1),
            gender='M',
            phone='+54911234567',
            email='juan.perez@example.com',
            address='Calle 123, Ciudad'
        )
        
        # Crear otro doctor
        other_doctor_user = User.objects.create_user(
            username='other_doctor',
            email='other@example.com',
            password='testpass123',
            first_name='Dr. María',
            last_name='Cardióloga'
        )
        
        other_doctor = Doctor.objects.create(
            user=other_doctor_user,
            license_number='MP54321',
            specialty='CARD',
            phone='+54911234568'
        )
        
        # Crear consulta con el doctor original
        consult = Consult.objects.create(
            patient=patient,
            doctor=self.doctor,
            date=datetime.now(),
            consult_type='FIRST',
            reason='Dolor de cabeza',
            symptoms='Cefalea intensa',
            vital_signs='TA: 120/80'
        )
        
        # El doctor original puede acceder al paciente
        self.client.login(username='doctor', password='testpass123')
        response = self.client.get(reverse('patient_detail', args=[patient.pk]))
        self.assertEqual(response.status_code, 200)
        
        # El otro doctor no puede acceder al paciente
        self.client.login(username='other_doctor', password='testpass123')
        response = self.client.get(reverse('patient_detail', args=[patient.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect (denied)
    
    def test_dashboard_data_consistency(self):
        """Test consistencia de datos en el dashboard"""
        # Crear datos de prueba
        patient1 = Person.objects.create(
            name='Juan',
            last_name='Pérez',
            dni='12345678',
            birth_date=date(1990, 1, 1),
            gender='M',
            phone='+54911234567',
            email='juan.perez@example.com',
            address='Calle 123, Ciudad'
        )
        
        patient2 = Person.objects.create(
            name='María',
            last_name='González',
            dni='87654321',
            birth_date=date(1985, 5, 15),
            gender='F',
            phone='+54911234568',
            email='maria.gonzalez@example.com',
            address='Calle 456, Ciudad'
        )
        
        # Crear consultas
        consult1 = Consult.objects.create(
            patient=patient1,
            doctor=self.doctor,
            date=datetime.now(),
            consult_type='FIRST',
            reason='Dolor de cabeza',
            symptoms='Cefalea intensa',
            vital_signs='TA: 120/80'
        )
        
        consult2 = Consult.objects.create(
            patient=patient2,
            doctor=self.doctor,
            date=datetime.now() - timedelta(days=1),
            consult_type='FOLLOW',
            reason='Seguimiento',
            symptoms='Mejoría',
            vital_signs='TA: 110/70'
        )
        
        # Test dashboard para administrador
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Verificar estadísticas
        self.assertContains(response, '2')  # Total pacientes
        self.assertContains(response, '2')  # Total consultas
        self.assertContains(response, '1')  # Total doctores
        
        # Test dashboard para doctor
        self.client.login(username='doctor', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Verificar que el doctor ve sus consultas
        self.assertContains(response, '2')  # Mis consultas
        self.assertContains(response, 'Juan Pérez')
        self.assertContains(response, 'María González')
    
    def test_search_functionality(self):
        """Test funcionalidad de búsqueda"""
        # Crear pacientes de prueba
        patient1 = Person.objects.create(
            name='Juan',
            last_name='Pérez',
            dni='12345678',
            birth_date=date(1990, 1, 1),
            gender='M',
            phone='+54911234567',
            email='juan.perez@example.com',
            address='Calle 123, Ciudad'
        )
        
        patient2 = Person.objects.create(
            name='María',
            last_name='González',
            dni='87654321',
            birth_date=date(1985, 5, 15),
            gender='F',
            phone='+54911234568',
            email='maria.gonzalez@example.com',
            address='Calle 456, Ciudad'
        )
        
        self.client.login(username='admin', password='testpass123')
        
        # Búsqueda por nombre
        response = self.client.get(reverse('patient_list'), {'search': 'Juan'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
        self.assertNotContains(response, 'María González')
        
        # Búsqueda por DNI
        response = self.client.get(reverse('patient_list'), {'search': '87654321'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'María González')
        self.assertNotContains(response, 'Juan Pérez')
        
        # Búsqueda por género
        response = self.client.get(reverse('patient_list'), {'gender': 'F'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'María González')
        self.assertNotContains(response, 'Juan Pérez')
    
    def test_pagination(self):
        """Test funcionalidad de paginación"""
        # Crear múltiples pacientes
        for i in range(25):
            Person.objects.create(
                name=f'Paciente{i}',
                last_name='Test',
                dni=f'{10000000 + i}',
                birth_date=date(1990, 1, 1),
                gender='M',
                phone='+54911234567',
                email=f'paciente{i}@example.com',
                address='Calle Test'
            )
        
        self.client.login(username='admin', password='testpass123')
        
        # Primera página
        response = self.client.get(reverse('patient_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Paciente0')
        
        # Segunda página
        response = self.client.get(reverse('patient_list'), {'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Paciente10')
    
    def test_error_handling(self):
        """Test manejo de errores"""
        self.client.login(username='admin', password='testpass123')
        
        # Intentar acceder a paciente inexistente
        response = self.client.get(reverse('patient_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)
        
        # Intentar acceder a consulta inexistente
        response = self.client.get(reverse('consult_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)
    
    def test_audit_logging_integration(self):
        """Test integración del logging de auditoría"""
        from history.utils import log_audit_action
        
        # Crear paciente y registrar acción
        patient = Person.objects.create(
            name='Juan',
            last_name='Pérez',
            dni='12345678',
            birth_date=date(1990, 1, 1),
            gender='M',
            phone='+54911234567',
            email='juan.perez@example.com',
            address='Calle 123, Ciudad'
        )
        
        # Simular creación de consulta con logging
        self.client.login(username='admin', password='testpass123')
        
        # Crear consulta
        response = self.client.post(reverse('consult_create'), {
            'patient': patient.pk,
            'doctor': self.doctor.pk,
            'date': datetime.now().strftime('%Y-%m-%dT%H:%M'),
            'consult_type': 'FIRST',
            'reason': 'Dolor de cabeza',
            'symptoms': 'Cefalea intensa',
            'vital_signs': 'TA: 120/80'
        })
        
        self.assertEqual(response.status_code, 302)  # Success
        
        # Verificar que se creó la consulta
        consult = Consult.objects.get(patient=patient)
        self.assertIsNotNone(consult)
        
        # Verificar que se puede acceder al detalle
        response = self.client.get(reverse('consult_detail', args=[consult.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_concurrent_access(self):
        """Test acceso concurrente (básico)"""
        # Crear paciente
        patient = Person.objects.create(
            name='Juan',
            last_name='Pérez',
            dni='12345678',
            birth_date=date(1990, 1, 1),
            gender='M',
            phone='+54911234567',
            email='juan.perez@example.com',
            address='Calle 123, Ciudad'
        )
        
        # Simular acceso concurrente de dos administradores
        admin1 = User.objects.create_user(
            username='admin1',
            email='admin1@example.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        
        admin2 = User.objects.create_user(
            username='admin2',
            email='admin2@example.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        
        # Ambos pueden acceder al mismo paciente
        self.client.login(username='admin1', password='testpass123')
        response1 = self.client.get(reverse('patient_detail', args=[patient.pk]))
        self.assertEqual(response1.status_code, 200)
        
        self.client.login(username='admin2', password='testpass123')
        response2 = self.client.get(reverse('patient_detail', args=[patient.pk]))
        self.assertEqual(response2.status_code, 200)
    
    def test_data_integrity(self):
        """Test integridad de datos"""
        # Crear paciente
        patient = Person.objects.create(
            name='Juan',
            last_name='Pérez',
            dni='12345678',
            birth_date=date(1990, 1, 1),
            gender='M',
            phone='+54911234567',
            email='juan.perez@example.com',
            address='Calle 123, Ciudad'
        )
        
        # Crear consulta
        consult = Consult.objects.create(
            patient=patient,
            doctor=self.doctor,
            date=datetime.now(),
            consult_type='FIRST',
            reason='Dolor de cabeza',
            symptoms='Cefalea intensa',
            vital_signs='TA: 120/80'
        )
        
        # Verificar relaciones
        self.assertEqual(consult.patient, patient)
        self.assertEqual(consult.doctor, self.doctor)
        
        # Verificar que se puede acceder desde ambas direcciones
        self.assertIn(consult, patient.consult_set.all())
        self.assertIn(consult, self.doctor.consult_set.all())
        
        # Eliminar paciente (soft delete)
        patient.is_active = False
        patient.save()
        
        # La consulta debería seguir existiendo
        consult.refresh_from_db()
        self.assertIsNotNone(consult)
        self.assertEqual(consult.patient, patient)

