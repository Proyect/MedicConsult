import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from history.models import Person, Doctor, Consult, UserProfile
from datetime import date, datetime, timedelta
import json


class AuthenticationViewsTest(TestCase):
    """Tests para las vistas de autenticación"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_login_view_get(self):
        """Test GET request a login view"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'login')
    
    def test_login_view_post_valid_credentials(self):
        """Test POST request con credenciales válidas"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
        self.assertRedirects(response, reverse('dashboard'))
    
    def test_login_view_post_invalid_credentials(self):
        """Test POST request con credenciales inválidas"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Credenciales inválidas')
    
    def test_login_view_authenticated_user_redirect(self):
        """Test que usuario autenticado es redirigido"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
    
    def test_logout_view(self):
        """Test logout view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))


class DashboardViewTest(TestCase):
    """Tests para la vista del dashboard"""
    
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
        
        # Crear pacientes
        self.patient1 = Person.objects.create(
            name='Juan',
            last_name='Pérez',
            dni='12345678',
            birth_date=date(1990, 1, 1),
            gender='M',
            phone='+54911234567',
            email='juan.perez@example.com',
            address='Calle 123, Ciudad'
        )
        
        self.patient2 = Person.objects.create(
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
        self.consult1 = Consult.objects.create(
            patient=self.patient1,
            doctor=self.doctor,
            date=datetime.now(),
            consult_type='FIRST',
            reason='Dolor de cabeza',
            symptoms='Cefalea intensa',
            vital_signs='TA: 120/80'
        )
        
        self.consult2 = Consult.objects.create(
            patient=self.patient2,
            doctor=self.doctor,
            date=datetime.now() - timedelta(days=1),
            consult_type='FOLLOW',
            reason='Seguimiento',
            symptoms='Mejoría',
            vital_signs='TA: 110/70'
        )
    
    def test_dashboard_admin_user(self):
        """Test dashboard para usuario administrador"""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
        self.assertContains(response, '2')  # Total pacientes
        self.assertContains(response, '2')  # Total consultas
        self.assertContains(response, '1')  # Total doctores
    
    def test_dashboard_doctor_user(self):
        """Test dashboard para usuario doctor"""
        self.client.login(username='doctor', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
        self.assertContains(response, '2')  # Mis consultas
        self.assertContains(response, 'Dr. Juan Médico')  # Nombre del doctor
    
    def test_dashboard_unauthenticated_user(self):
        """Test dashboard para usuario no autenticado"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")
    
    def test_dashboard_data_api(self):
        """Test API de datos del dashboard"""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('dashboard_data_api'))
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('total_patients', data)
        self.assertIn('total_consults', data)


class PatientViewsTest(TestCase):
    """Tests para las vistas de pacientes"""
    
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
        
        # Crear consulta para el doctor
        self.consult = Consult.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date=datetime.now(),
            consult_type='FIRST',
            reason='Dolor de cabeza',
            symptoms='Cefalea intensa',
            vital_signs='TA: 120/80'
        )
    
    def test_patient_list_admin(self):
        """Test lista de pacientes para administrador"""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('patient_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
        self.assertContains(response, '12345678')
    
    def test_patient_list_doctor(self):
        """Test lista de pacientes para doctor"""
        self.client.login(username='doctor', password='testpass123')
        response = self.client.get(reverse('patient_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')  # Su paciente
    
    def test_patient_list_unauthenticated(self):
        """Test lista de pacientes sin autenticación"""
        response = self.client.get(reverse('patient_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_patient_detail_admin(self):
        """Test detalle de paciente para administrador"""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('patient_detail', args=[self.patient.pk]))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
        self.assertContains(response, '12345678')
    
    def test_patient_detail_doctor_with_access(self):
        """Test detalle de paciente para doctor con acceso"""
        self.client.login(username='doctor', password='testpass123')
        response = self.client.get(reverse('patient_detail', args=[self.patient.pk]))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
    
    def test_patient_create_admin(self):
        """Test crear paciente como administrador"""
        self.client.login(username='admin', password='testpass123')
        
        response = self.client.get(reverse('patient_create'))
        self.assertEqual(response.status_code, 200)
        
        # Crear nuevo paciente
        response = self.client.post(reverse('patient_create'), {
            'name': 'María',
            'last_name': 'González',
            'dni': '87654321',
            'birth_date': '1985-05-15',
            'gender': 'F',
            'phone': '+54911234568',
            'email': 'maria.gonzalez@example.com',
            'address': 'Calle 456, Ciudad',
            'observations': 'Paciente nuevo'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Person.objects.filter(dni='87654321').exists())
    
    def test_patient_create_doctor_denied(self):
        """Test que doctor no puede crear pacientes"""
        self.client.login(username='doctor', password='testpass123')
        response = self.client.get(reverse('patient_create'))
        self.assertEqual(response.status_code, 302)  # Redirect (denied)
    
    def test_patient_edit_admin(self):
        """Test editar paciente como administrador"""
        self.client.login(username='admin', password='testpass123')
        
        response = self.client.get(reverse('patient_edit', args=[self.patient.pk]))
        self.assertEqual(response.status_code, 200)
        
        # Editar paciente
        response = self.client.post(reverse('patient_edit', args=[self.patient.pk]), {
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
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.name, 'Juan Carlos')
    
    def test_patient_delete_admin(self):
        """Test eliminar paciente como administrador"""
        self.client.login(username='admin', password='testpass123')
        
        response = self.client.get(reverse('patient_delete', args=[self.patient.pk]))
        self.assertEqual(response.status_code, 200)
        
        # Eliminar paciente (soft delete)
        response = self.client.post(reverse('patient_delete', args=[self.patient.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        
        self.patient.refresh_from_db()
        self.assertFalse(self.patient.is_active)


class ConsultViewsTest(TestCase):
    """Tests para las vistas de consultas"""
    
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
        
        # Crear consulta
        self.consult = Consult.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date=datetime.now(),
            consult_type='FIRST',
            reason='Dolor de cabeza',
            symptoms='Cefalea intensa',
            vital_signs='TA: 120/80'
        )
    
    def test_consult_list_admin(self):
        """Test lista de consultas para administrador"""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('consult_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
    
    def test_consult_list_doctor(self):
        """Test lista de consultas para doctor"""
        self.client.login(username='doctor', password='testpass123')
        response = self.client.get(reverse('consult_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
    
    def test_consult_detail_admin(self):
        """Test detalle de consulta para administrador"""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('consult_detail', args=[self.consult.pk]))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
        self.assertContains(response, 'Dolor de cabeza')
    
    def test_consult_detail_doctor(self):
        """Test detalle de consulta para doctor"""
        self.client.login(username='doctor', password='testpass123')
        response = self.client.get(reverse('consult_detail', args=[self.consult.pk]))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
    
    def test_consult_create_admin(self):
        """Test crear consulta como administrador"""
        self.client.login(username='admin', password='testpass123')
        
        response = self.client.get(reverse('consult_create'))
        self.assertEqual(response.status_code, 200)
        
        # Crear nueva consulta
        response = self.client.post(reverse('consult_create'), {
            'patient': self.patient.pk,
            'doctor': self.doctor.pk,
            'date': datetime.now().strftime('%Y-%m-%dT%H:%M'),
            'consult_type': 'FOLLOW',
            'reason': 'Seguimiento',
            'symptoms': 'Mejoría',
            'vital_signs': 'TA: 110/70'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Consult.objects.filter(reason='Seguimiento').exists())
    
    def test_consult_create_doctor(self):
        """Test crear consulta como doctor"""
        self.client.login(username='doctor', password='testpass123')
        
        response = self.client.get(reverse('consult_create'))
        self.assertEqual(response.status_code, 200)
        
        # Crear nueva consulta
        response = self.client.post(reverse('consult_create'), {
            'patient': self.patient.pk,
            'doctor': self.doctor.pk,
            'date': datetime.now().strftime('%Y-%m-%dT%H:%M'),
            'consult_type': 'FOLLOW',
            'reason': 'Seguimiento',
            'symptoms': 'Mejoría',
            'vital_signs': 'TA: 110/70'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Consult.objects.filter(reason='Seguimiento').exists())


class DoctorViewsTest(TestCase):
    """Tests para las vistas de doctores"""
    
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
        
        # Crear doctor existente
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
    
    def test_doctor_list_admin(self):
        """Test lista de doctores para administrador"""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('doctor_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dr. Juan Médico')
    
    def test_doctor_list_doctor_denied(self):
        """Test que doctor no puede ver lista de doctores"""
        self.client.login(username='doctor', password='testpass123')
        response = self.client.get(reverse('doctor_list'))
        self.assertEqual(response.status_code, 302)  # Redirect (denied)
    
    def test_doctor_create_admin(self):
        """Test crear doctor como administrador"""
        self.client.login(username='admin', password='testpass123')
        
        response = self.client.get(reverse('doctor_create'))
        self.assertEqual(response.status_code, 200)
        
        # Crear nuevo doctor
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
        self.assertTrue(Doctor.objects.filter(license_number='MP54321').exists())
    
    def test_doctor_create_doctor_denied(self):
        """Test que doctor no puede crear doctores"""
        self.client.login(username='doctor', password='testpass123')
        response = self.client.get(reverse('doctor_create'))
        self.assertEqual(response.status_code, 302)  # Redirect (denied)

