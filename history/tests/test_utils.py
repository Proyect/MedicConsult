import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from history.models import Person, Doctor, Consult, UserProfile
from history.utils import (
    is_administrator, is_doctor, get_doctor_profile, 
    can_access_patient, can_access_consult, get_user_role, 
    require_role, is_patient, get_user_profile
)
from datetime import date, datetime


class UtilsTest(TestCase):
    """Tests para las funciones utilitarias"""
    
    def setUp(self):
        # Crear usuarios de prueba
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        
        self.doctor_user = User.objects.create_user(
            username='doctor',
            email='doctor@example.com',
            password='testpass123',
            first_name='Dr. Juan',
            last_name='Médico'
        )
        
        self.patient_user = User.objects.create_user(
            username='patient',
            email='patient@example.com',
            password='testpass123'
        )
        
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='testpass123'
        )
        
        # Crear perfil de doctor
        self.doctor = Doctor.objects.create(
            user=self.doctor_user,
            license_number='MP12345',
            specialty='GP',
            phone='+54911234567'
        )
        
        # Crear perfil de paciente
        self.patient_profile = UserProfile.objects.create(
            user=self.patient_user,
            role='PATIENT',
            phone='+54911234568'
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
    
    def test_is_administrator(self):
        """Test función is_administrator"""
        self.assertTrue(is_administrator(self.admin_user))
        self.assertFalse(is_administrator(self.doctor_user))
        self.assertFalse(is_administrator(self.patient_user))
        self.assertFalse(is_administrator(self.regular_user))
        self.assertFalse(is_administrator(None))
    
    def test_is_doctor(self):
        """Test función is_doctor"""
        self.assertFalse(is_doctor(self.admin_user))
        self.assertTrue(is_doctor(self.doctor_user))
        self.assertFalse(is_doctor(self.patient_user))
        self.assertFalse(is_doctor(self.regular_user))
        self.assertFalse(is_doctor(None))
    
    def test_get_doctor_profile(self):
        """Test función get_doctor_profile"""
        self.assertIsNone(get_doctor_profile(self.admin_user))
        self.assertEqual(get_doctor_profile(self.doctor_user), self.doctor)
        self.assertIsNone(get_doctor_profile(self.patient_user))
        self.assertIsNone(get_doctor_profile(self.regular_user))
        self.assertIsNone(get_doctor_profile(None))
    
    def test_is_patient(self):
        """Test función is_patient"""
        self.assertFalse(is_patient(self.admin_user))
        self.assertFalse(is_patient(self.doctor_user))
        self.assertTrue(is_patient(self.patient_user))
        self.assertFalse(is_patient(self.regular_user))
        self.assertFalse(is_patient(None))
    
    def test_get_user_profile(self):
        """Test función get_user_profile"""
        # Usuario con perfil existente
        profile = get_user_profile(self.patient_user)
        self.assertEqual(profile, self.patient_profile)
        
        # Usuario sin perfil (debe crear uno)
        profile = get_user_profile(self.regular_user)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user, self.regular_user)
        self.assertEqual(profile.role, 'PATIENT')
    
    def test_get_user_role(self):
        """Test función get_user_role"""
        self.assertEqual(get_user_role(self.admin_user), 'administrator')
        self.assertEqual(get_user_role(self.doctor_user), 'doctor')
        self.assertEqual(get_user_role(self.patient_user), 'patient')
        self.assertEqual(get_user_role(self.regular_user), 'patient')
        self.assertEqual(get_user_role(None), 'patient')
    
    def test_can_access_patient_admin(self):
        """Test que los administradores pueden acceder a todos los pacientes"""
        self.assertTrue(can_access_patient(self.admin_user, self.patient))
    
    def test_can_access_patient_doctor_with_consult(self):
        """Test que los doctores pueden acceder a sus pacientes"""
        self.assertTrue(can_access_patient(self.doctor_user, self.patient))
    
    def test_can_access_patient_doctor_without_consult(self):
        """Test que los doctores no pueden acceder a pacientes sin consultas"""
        # Crear otro paciente sin consultas con este doctor
        other_patient = Person.objects.create(
            name='María',
            last_name='González',
            dni='87654321',
            birth_date=date(1985, 5, 15),
            gender='F',
            phone='+54911234568',
            email='maria.gonzalez@example.com',
            address='Calle 456, Ciudad'
        )
        self.assertFalse(can_access_patient(self.doctor_user, other_patient))
    
    def test_can_access_patient_patient(self):
        """Test que los pacientes no pueden acceder a otros pacientes"""
        self.assertFalse(can_access_patient(self.patient_user, self.patient))
    
    def test_can_access_patient_invalid_inputs(self):
        """Test con entradas inválidas"""
        self.assertFalse(can_access_patient(None, self.patient))
        self.assertFalse(can_access_patient(self.doctor_user, None))
        self.assertFalse(can_access_patient(None, None))
    
    def test_can_access_consult_admin(self):
        """Test que los administradores pueden acceder a todas las consultas"""
        self.assertTrue(can_access_consult(self.admin_user, self.consult))
    
    def test_can_access_consult_doctor_own_consult(self):
        """Test que los doctores pueden acceder a sus propias consultas"""
        self.assertTrue(can_access_consult(self.doctor_user, self.consult))
    
    def test_can_access_consult_doctor_other_consult(self):
        """Test que los doctores no pueden acceder a consultas de otros doctores"""
        # Crear otro doctor y consulta
        other_doctor_user = User.objects.create_user(
            username='other_doctor',
            email='other@example.com',
            password='testpass123'
        )
        other_doctor = Doctor.objects.create(
            user=other_doctor_user,
            license_number='MP54321',
            specialty='CARD',
            phone='+54911234569'
        )
        
        other_consult = Consult.objects.create(
            patient=self.patient,
            doctor=other_doctor,
            date=datetime.now(),
            consult_type='FIRST',
            reason='Dolor de pecho',
            symptoms='Dolor precordial',
            vital_signs='TA: 140/90'
        )
        
        self.assertFalse(can_access_consult(self.doctor_user, other_consult))
    
    def test_can_access_consult_patient(self):
        """Test que los pacientes no pueden acceder a consultas"""
        self.assertFalse(can_access_consult(self.patient_user, self.consult))
    
    def test_can_access_consult_invalid_inputs(self):
        """Test con entradas inválidas"""
        self.assertFalse(can_access_consult(None, self.consult))
        self.assertFalse(can_access_consult(self.doctor_user, None))
        self.assertFalse(can_access_consult(None, None))
    
    def test_require_role_decorator_administrator(self):
        """Test decorator require_role para administrador"""
        from django.test import RequestFactory
        from history.views import dashboard
        
        factory = RequestFactory()
        request = factory.get('/')
        request.user = self.admin_user
        
        # El decorator debería permitir el acceso
        response = dashboard(request)
        self.assertEqual(response.status_code, 200)
    
    def test_require_role_decorator_doctor(self):
        """Test decorator require_role para doctor"""
        from django.test import RequestFactory
        from history.views import patient_list
        
        factory = RequestFactory()
        request = factory.get('/patients/')
        request.user = self.doctor_user
        
        # El decorator debería permitir el acceso
        response = patient_list(request)
        self.assertEqual(response.status_code, 200)
    
    def test_require_role_decorator_patient_denied(self):
        """Test decorator require_role deniega acceso a paciente"""
        from django.test import RequestFactory
        from history.views import patient_create
        
        factory = RequestFactory()
        request = factory.get('/patients/create/')
        request.user = self.patient_user
        
        # El decorator debería denegar el acceso
        response = patient_create(request)
        self.assertEqual(response.status_code, 302)  # Redirect

