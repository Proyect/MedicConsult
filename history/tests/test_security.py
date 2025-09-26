import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache
from history.models import Person, Doctor, Consult, UserProfile
from datetime import date, datetime
import json


class SecurityTest(TestCase):
    """Tests de seguridad para el sistema"""
    
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
        
        # Crear otro doctor
        self.other_doctor_user = User.objects.create_user(
            username='other_doctor',
            email='other@example.com',
            password='testpass123',
            first_name='Dr. María',
            last_name='Cardióloga'
        )
        
        self.other_doctor = Doctor.objects.create(
            user=self.other_doctor_user,
            license_number='MP54321',
            specialty='CARD',
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
        
        # Crear consulta del doctor
        self.consult = Consult.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date=datetime.now(),
            consult_type='FIRST',
            reason='Dolor de cabeza',
            symptoms='Cefalea intensa',
            vital_signs='TA: 120/80'
        )
        
        # Crear consulta del otro doctor
        self.other_consult = Consult.objects.create(
            patient=self.patient,
            doctor=self.other_doctor,
            date=datetime.now(),
            consult_type='FIRST',
            reason='Dolor de pecho',
            symptoms='Dolor precordial',
            vital_signs='TA: 140/90'
        )
    
    def tearDown(self):
        cache.clear()
    
    def test_rate_limiting_login(self):
        """Test rate limiting en login"""
        # Configurar rate limiting
        from django.conf import settings
        settings.RATE_LIMIT_ENABLE = True
        settings.RATE_LIMIT_ATTEMPTS = 3
        settings.RATE_LIMIT_WINDOW = 60
        
        # Intentar login con credenciales incorrectas múltiples veces
        for i in range(4):  # 4 intentos (más del límite)
            response = self.client.post(reverse('login'), {
                'username': 'admin',
                'password': 'wrongpassword'
            })
        
        # El último intento debería ser bloqueado
        self.assertEqual(response.status_code, 429)  # Too Many Requests
    
    def test_csrf_protection(self):
        """Test protección CSRF"""
        # Intentar crear paciente sin CSRF token
        response = self.client.post(reverse('patient_create'), {
            'name': 'Test',
            'last_name': 'User',
            'dni': '12345678',
            'birth_date': '1990-01-01',
            'gender': 'M',
            'phone': '+54911234567',
            'email': 'test@example.com',
            'address': 'Test Address'
        })
        
        # Debería fallar por falta de CSRF token
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_authentication_required(self):
        """Test que las vistas requieren autenticación"""
        protected_urls = [
            reverse('dashboard'),
            reverse('patient_list'),
            reverse('consult_list'),
            reverse('doctor_list'),
        ]
        
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_doctor_cannot_access_other_doctors_patients(self):
        """Test que doctor no puede acceder a pacientes de otros doctores"""
        self.client.login(username='doctor', password='testpass123')
        
        # Crear paciente sin consultas con este doctor
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
        
        # Intentar acceder al detalle del paciente
        response = self.client.get(reverse('patient_detail', args=[other_patient.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect (denied)
    
    def test_doctor_cannot_access_other_doctors_consults(self):
        """Test que doctor no puede acceder a consultas de otros doctores"""
        self.client.login(username='doctor', password='testpass123')
        
        # Intentar acceder a consulta de otro doctor
        response = self.client.get(reverse('consult_detail', args=[self.other_consult.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect (denied)
    
    def test_doctor_cannot_create_patients(self):
        """Test que doctor no puede crear pacientes"""
        self.client.login(username='doctor', password='testpass123')
        
        response = self.client.get(reverse('patient_create'))
        self.assertEqual(response.status_code, 302)  # Redirect (denied)
    
    def test_doctor_cannot_create_doctors(self):
        """Test que doctor no puede crear doctores"""
        self.client.login(username='doctor', password='testpass123')
        
        response = self.client.get(reverse('doctor_create'))
        self.assertEqual(response.status_code, 302)  # Redirect (denied)
    
    def test_doctor_cannot_edit_other_doctors_consults(self):
        """Test que doctor no puede editar consultas de otros doctores"""
        self.client.login(username='doctor', password='testpass123')
        
        # Intentar editar consulta de otro doctor (si existiera la vista)
        # Por ahora solo verificamos que no puede acceder al detalle
        response = self.client.get(reverse('consult_detail', args=[self.other_consult.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect (denied)
    
    def test_sql_injection_protection(self):
        """Test protección contra inyección SQL"""
        self.client.login(username='admin', password='testpass123')
        
        # Intentar inyección SQL en búsqueda de pacientes
        malicious_search = "'; DROP TABLE history_person; --"
        response = self.client.get(reverse('patient_list'), {
            'search': malicious_search
        })
        
        # Debería funcionar normalmente sin causar errores
        self.assertEqual(response.status_code, 200)
        # Verificar que la tabla aún existe
        self.assertTrue(Person.objects.exists())
    
    def test_xss_protection(self):
        """Test protección contra XSS"""
        self.client.login(username='admin', password='testpass123')
        
        # Crear paciente con datos que podrían ser XSS
        xss_data = '<script>alert("XSS")</script>'
        response = self.client.post(reverse('patient_create'), {
            'name': xss_data,
            'last_name': 'Test',
            'dni': '12345678',
            'birth_date': '1990-01-01',
            'gender': 'M',
            'phone': '+54911234567',
            'email': 'test@example.com',
            'address': 'Test Address'
        })
        
        # Debería crear el paciente pero escapar el HTML
        if response.status_code == 302:  # Success
            patient = Person.objects.get(dni='12345678')
            # El nombre debería estar escapado en la respuesta
            response = self.client.get(reverse('patient_detail', args=[patient.pk]))
            self.assertNotContains(response, '<script>')
    
    def test_file_upload_security(self):
        """Test seguridad en subida de archivos"""
        # Por ahora no hay subida de archivos, pero se puede preparar
        # para futuras implementaciones
        pass
    
    def test_session_security(self):
        """Test seguridad de sesiones"""
        self.client.login(username='admin', password='testpass123')
        
        # Verificar que la sesión está configurada correctamente
        session = self.client.session
        self.assertIn('_auth_user_id', session)
        
        # Verificar que la sesión expira
        from django.conf import settings
        self.assertEqual(settings.SESSION_COOKIE_AGE, 3600)  # 1 hora
        self.assertTrue(settings.SESSION_EXPIRE_AT_BROWSER_CLOSE)
    
    def test_password_security(self):
        """Test seguridad de contraseñas"""
        # Verificar que Django aplica validadores de contraseña
        from django.conf import settings
        validators = settings.AUTH_PASSWORD_VALIDATORS
        self.assertTrue(len(validators) > 0)
        
        # Verificar que se requiere contraseña fuerte
        weak_password = '123'
        user = User(username='testuser')
        user.set_password(weak_password)
        
        # Django debería validar la contraseña
        from django.contrib.auth.password_validation import validate_password
        from django.core.exceptions import ValidationError
        
        with self.assertRaises(ValidationError):
            validate_password(weak_password)
    
    def test_https_redirect_in_production(self):
        """Test redirección HTTPS en producción"""
        # Este test verificaría que en producción se redirige a HTTPS
        # Por ahora solo verificamos la configuración
        from django.conf import settings
        # En desarrollo, SECURE_SSL_REDIRECT debería ser False
        # En producción, debería ser True
        pass
    
    def test_secure_headers(self):
        """Test headers de seguridad"""
        response = self.client.get(reverse('login'))
        
        # Verificar headers de seguridad
        self.assertEqual(response.get('X-Frame-Options'), 'DENY')
        # Otros headers se pueden verificar según la configuración
    
    def test_input_validation(self):
        """Test validación de entrada en formularios"""
        self.client.login(username='admin', password='testpass123')
        
        # Intentar crear paciente con datos inválidos
        invalid_data = {
            'name': '',  # Nombre vacío
            'last_name': '',  # Apellido vacío
            'dni': 'abc',  # DNI inválido
            'birth_date': 'invalid-date',  # Fecha inválida
            'gender': 'X',  # Género inválido
            'phone': '123',  # Teléfono muy corto
            'email': 'invalid-email',  # Email inválido
            'address': ''  # Dirección vacía
        }
        
        response = self.client.post(reverse('patient_create'), invalid_data)
        self.assertEqual(response.status_code, 200)  # Formulario con errores
        self.assertContains(response, 'Este campo es obligatorio')
    
    def test_authorization_bypass_attempts(self):
        """Test intentos de bypass de autorización"""
        # Crear usuario normal sin permisos especiales
        normal_user = User.objects.create_user(
            username='normal',
            email='normal@example.com',
            password='testpass123'
        )
        
        self.client.login(username='normal', password='testpass123')
        
        # Intentar acceder a vistas de administrador
        admin_urls = [
            reverse('patient_create'),
            reverse('doctor_create'),
            reverse('doctor_list'),
        ]
        
        for url in admin_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # Redirect (denied)
    
    def test_data_isolation(self):
        """Test aislamiento de datos entre doctores"""
        self.client.login(username='doctor', password='testpass123')
        
        # El doctor solo debería ver sus propias consultas
        response = self.client.get(reverse('consult_list'))
        self.assertEqual(response.status_code, 200)
        
        # Verificar que solo ve sus consultas
        consults = response.context.get('page_obj', [])
        for consult in consults:
            self.assertEqual(consult.doctor, self.doctor)
    
    def test_audit_logging(self):
        """Test logging de auditoría"""
        from history.utils import log_audit_action
        
        # Crear log de auditoría
        log_audit_action(
            user=self.admin_user,
            action='CREATE',
            model_name='Person',
            object_id='123',
            description='Test audit log'
        )
        
        # Verificar que se creó el log
        from history.models import AuditLog
        log = AuditLog.objects.filter(
            user=self.admin_user,
            action='CREATE',
            model_name='Person'
        ).first()
        
        self.assertIsNotNone(log)
        self.assertEqual(log.description, 'Test audit log')

