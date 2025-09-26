import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from history.models import Person, Doctor, Consult, UserProfile
from datetime import date, datetime


class BasicFunctionalityTest(TestCase):
    """Tests básicos de funcionalidad del sistema"""
    
    def setUp(self):
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
    
    def test_admin_can_access_dashboard(self):
        """Test que el administrador puede acceder al dashboard"""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
    
    def test_doctor_can_access_dashboard(self):
        """Test que el doctor puede acceder al dashboard"""
        self.client.login(username='doctor', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
    
    def test_unauthenticated_user_redirected_to_login(self):
        """Test que usuario no autenticado es redirigido al login"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")
    
    def test_admin_can_create_patient(self):
        """Test que el administrador puede crear pacientes"""
        self.client.login(username='admin', password='testpass123')
        
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
    
    def test_doctor_can_create_consult(self):
        """Test que el doctor puede crear consultas"""
        self.client.login(username='doctor', password='testpass123')
        
        response = self.client.post(reverse('consult_create'), {
            'patient': self.patient.pk,
            'doctor': self.doctor.pk,
            'date': datetime.now().strftime('%Y-%m-%dT%H:%M'),
            'consult_type': 'FIRST',
            'reason': 'Dolor de cabeza',
            'symptoms': 'Cefalea intensa',
            'vital_signs': 'TA: 120/80'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Consult.objects.filter(patient=self.patient).exists())
    
    def test_patient_list_displays_patients(self):
        """Test que la lista de pacientes muestra los pacientes"""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('patient_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
        self.assertContains(response, '12345678')
    
    def test_consult_list_displays_consults(self):
        """Test que la lista de consultas muestra las consultas"""
        # Crear consulta
        Consult.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date=datetime.now(),
            consult_type='FIRST',
            reason='Dolor de cabeza',
            symptoms='Cefalea intensa',
            vital_signs='TA: 120/80'
        )
        
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('consult_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
        self.assertContains(response, 'Dolor de cabeza')
    
    def test_patient_detail_shows_patient_info(self):
        """Test que el detalle del paciente muestra la información correcta"""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('patient_detail', args=[self.patient.pk]))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
        self.assertContains(response, '12345678')
        self.assertContains(response, 'juan.perez@example.com')
    
    def test_consult_detail_shows_consult_info(self):
        """Test que el detalle de la consulta muestra la información correcta"""
        # Crear consulta
        consult = Consult.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date=datetime.now(),
            consult_type='FIRST',
            reason='Dolor de cabeza',
            symptoms='Cefalea intensa',
            vital_signs='TA: 120/80'
        )
        
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('consult_detail', args=[consult.pk]))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
        self.assertContains(response, 'Dolor de cabeza')
        self.assertContains(response, 'Cefalea intensa')
    
    def test_doctor_can_access_own_patients(self):
        """Test que el doctor puede acceder a sus propios pacientes"""
        # Crear consulta para que el doctor tenga acceso al paciente
        Consult.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date=datetime.now(),
            consult_type='FIRST',
            reason='Dolor de cabeza',
            symptoms='Cefalea intensa',
            vital_signs='TA: 120/80'
        )
        
        self.client.login(username='doctor', password='testpass123')
        response = self.client.get(reverse('patient_detail', args=[self.patient.pk]))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
    
    def test_doctor_cannot_access_other_doctors_patients(self):
        """Test que el doctor no puede acceder a pacientes de otros doctores"""
        # Crear otro doctor y paciente sin consultas
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
        
        other_patient = Person.objects.create(
            name='Ana',
            last_name='García',
            dni='87654321',
            birth_date=date(1985, 5, 15),
            gender='F',
            phone='+54911234568',
            email='ana.garcia@example.com',
            address='Calle 456, Ciudad'
        )
        
        # Crear consulta con el otro doctor
        Consult.objects.create(
            patient=other_patient,
            doctor=other_doctor,
            date=datetime.now(),
            consult_type='FIRST',
            reason='Dolor de pecho',
            symptoms='Dolor precordial',
            vital_signs='TA: 140/90'
        )
        
        # El doctor original no debería poder acceder al paciente del otro doctor
        self.client.login(username='doctor', password='testpass123')
        response = self.client.get(reverse('patient_detail', args=[other_patient.pk]))
        
        self.assertEqual(response.status_code, 302)  # Redirect (denied)
    
    def test_dashboard_shows_correct_statistics(self):
        """Test que el dashboard muestra las estadísticas correctas"""
        # Crear más datos de prueba
        Person.objects.create(
            name='María',
            last_name='González',
            dni='87654321',
            birth_date=date(1985, 5, 15),
            gender='F',
            phone='+54911234568',
            email='maria.gonzalez@example.com',
            address='Calle 456, Ciudad'
        )
        
        Consult.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date=datetime.now(),
            consult_type='FIRST',
            reason='Dolor de cabeza',
            symptoms='Cefalea intensa',
            vital_signs='TA: 120/80'
        )
        
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2')  # Total pacientes
        self.assertContains(response, '1')  # Total consultas
        self.assertContains(response, '1')  # Total doctores
    
    def test_search_functionality_works(self):
        """Test que la funcionalidad de búsqueda funciona"""
        self.client.login(username='admin', password='testpass123')
        
        # Búsqueda por nombre
        response = self.client.get(reverse('patient_list'), {'search': 'Juan'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
        
        # Búsqueda por DNI
        response = self.client.get(reverse('patient_list'), {'search': '12345678'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
    
    def test_forms_work_correctly(self):
        """Test que los formularios funcionan correctamente"""
        self.client.login(username='admin', password='testpass123')
        
        # Test formulario de paciente
        response = self.client.get(reverse('patient_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        
        # Test formulario de consulta
        response = self.client.get(reverse('consult_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
    
    def test_models_work_correctly(self):
        """Test que los modelos funcionan correctamente"""
        # Test Person model
        self.assertEqual(str(self.patient), 'Juan Pérez - DNI: 12345678')
        self.assertEqual(self.patient.age, 34)  # Aproximadamente
        
        # Test Doctor model
        self.assertEqual(str(self.doctor), 'Dr. Dr. Juan Médico - Medicina General')
        self.assertEqual(self.doctor.full_name, 'Dr. Juan Médico')
        
        # Test Consult model
        consult = Consult.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date=datetime.now(),
            consult_type='FIRST',
            reason='Dolor de cabeza',
            symptoms='Cefalea intensa',
            vital_signs='TA: 120/80'
        )
        
        self.assertIn('Consulta', str(consult))
        self.assertIn('Juan Pérez', str(consult))
        self.assertIn('Dr. Dr. Juan Médico', str(consult))

