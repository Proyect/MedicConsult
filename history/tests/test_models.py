import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
from history.models import Person, Doctor, Consult, Diagnosis, Treatment, MedicalRecord, UserProfile, AuditLog


class PersonModelTest(TestCase):
    """Tests para el modelo Person"""
    
    def setUp(self):
        self.person_data = {
            'name': 'Juan',
            'last_name': 'Pérez',
            'dni': '12345678',
            'birth_date': date(1990, 1, 1),
            'gender': 'M',
            'phone': '+54911234567',
            'email': 'juan.perez@example.com',
            'address': 'Calle 123, Ciudad',
            'observations': 'Paciente regular'
        }
    
    def test_create_person(self):
        """Test crear una persona correctamente"""
        person = Person.objects.create(**self.person_data)
        self.assertEqual(person.name, 'Juan')
        self.assertEqual(person.last_name, 'Pérez')
        self.assertEqual(person.dni, '12345678')
        self.assertTrue(person.is_active)
    
    def test_person_str_representation(self):
        """Test la representación string del modelo"""
        person = Person.objects.create(**self.person_data)
        expected = "Juan Pérez - DNI: 12345678"
        self.assertEqual(str(person), expected)
    
    def test_person_age_property(self):
        """Test la propiedad age"""
        person = Person.objects.create(**self.person_data)
        expected_age = date.today().year - 1990
        self.assertEqual(person.age, expected_age)
    
    def test_dni_unique_constraint(self):
        """Test que el DNI debe ser único"""
        Person.objects.create(**self.person_data)
        
        with self.assertRaises(IntegrityError):
            Person.objects.create(**self.person_data)
    
    def test_email_unique_constraint(self):
        """Test que el email debe ser único"""
        Person.objects.create(**self.person_data)
        
        with self.assertRaises(IntegrityError):
            Person.objects.create(
                name='María',
                last_name='González',
                dni='87654321',
                birth_date=date(1985, 5, 15),
                gender='F',
                phone='+54911234568',
                email='juan.perez@example.com',  # Mismo email
                address='Calle 456, Ciudad'
            )
    
    def test_dni_validation(self):
        """Test validación de DNI"""
        # DNI muy corto
        person_data = self.person_data.copy()
        person_data['dni'] = '123'
        person = Person(**person_data)
        with self.assertRaises(ValidationError):
            person.full_clean()
    
    def test_phone_validation(self):
        """Test validación de teléfono"""
        # Teléfono inválido
        person_data = self.person_data.copy()
        person_data['phone'] = '123'
        person = Person(**person_data)
        with self.assertRaises(ValidationError):
            person.full_clean()


class DoctorModelTest(TestCase):
    """Tests para el modelo Doctor"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='doctor1',
            email='doctor@example.com',
            password='testpass123',
            first_name='Dr. Juan',
            last_name='Médico'
        )
        self.doctor_data = {
            'user': self.user,
            'license_number': 'MP12345',
            'specialty': 'GP',
            'phone': '+54911234567',
            'is_active': True
        }
    
    def test_create_doctor(self):
        """Test crear un doctor correctamente"""
        doctor = Doctor.objects.create(**self.doctor_data)
        self.assertEqual(doctor.user, self.user)
        self.assertEqual(doctor.license_number, 'MP12345')
        self.assertEqual(doctor.specialty, 'GP')
        self.assertTrue(doctor.is_active)
    
    def test_doctor_str_representation(self):
        """Test la representación string del modelo"""
        doctor = Doctor.objects.create(**self.doctor_data)
        expected = "Dr. Dr. Juan Médico - Medicina General"
        self.assertEqual(str(doctor), expected)
    
    def test_doctor_full_name_property(self):
        """Test la propiedad full_name"""
        doctor = Doctor.objects.create(**self.doctor_data)
        self.assertEqual(doctor.full_name, "Dr. Juan Médico")
    
    def test_license_number_unique_constraint(self):
        """Test que el número de matrícula debe ser único"""
        Doctor.objects.create(**self.doctor_data)
        
        user2 = User.objects.create_user(
            username='doctor2',
            email='doctor2@example.com',
            password='testpass123'
        )
        
        with self.assertRaises(IntegrityError):
            Doctor.objects.create(
                user=user2,
                license_number='MP12345',  # Mismo número de matrícula
                specialty='CARD',
                phone='+54911234568'
            )


class ConsultModelTest(TestCase):
    """Tests para el modelo Consult"""
    
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
        
        self.consult_data = {
            'patient': self.patient,
            'doctor': self.doctor,
            'date': datetime.now(),
            'consult_type': 'FIRST',
            'reason': 'Dolor de cabeza',
            'symptoms': 'Cefalea intensa',
            'vital_signs': 'TA: 120/80, FC: 80'
        }
    
    def test_create_consult(self):
        """Test crear una consulta correctamente"""
        consult = Consult.objects.create(**self.consult_data)
        self.assertEqual(consult.patient, self.patient)
        self.assertEqual(consult.doctor, self.doctor)
        self.assertEqual(consult.consult_type, 'FIRST')
        self.assertEqual(consult.reason, 'Dolor de cabeza')
    
    def test_consult_str_representation(self):
        """Test la representación string del modelo"""
        consult = Consult.objects.create(**self.consult_data)
        expected_start = f"Consulta {consult.id} - Juan Pérez - DNI: 12345678 con Dr. Dr. Juan Médico"
        self.assertTrue(str(consult).startswith(expected_start))
    
    def test_consult_ordering(self):
        """Test que las consultas se ordenan por fecha descendente"""
        # Crear consultas con fechas diferentes
        consult1 = Consult.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date=datetime.now() - timedelta(days=1),
            consult_type='FIRST',
            reason='Dolor de cabeza',
            symptoms='Cefalea intensa',
            vital_signs='TA: 120/80'
        )
        consult2 = Consult.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date=datetime.now(),
            consult_type='FIRST',
            reason='Dolor de cabeza',
            symptoms='Cefalea intensa',
            vital_signs='TA: 120/80'
        )
        
        consults = Consult.objects.all()
        self.assertEqual(consults[0], consult2)  # Más reciente primero
        self.assertEqual(consults[1], consult1)


class MedicalRecordModelTest(TestCase):
    """Tests para el modelo MedicalRecord"""
    
    def setUp(self):
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
    
    def test_create_medical_record(self):
        """Test crear una historia clínica correctamente"""
        record = MedicalRecord.objects.create(
            patient=self.patient,
            allergies='Penicilina',
            chronic_conditions='Diabetes',
            family_history='Hipertensión en familia',
            social_history='No fuma, no bebe'
        )
        self.assertEqual(record.patient, self.patient)
        self.assertEqual(record.allergies, 'Penicilina')
        self.assertEqual(record.chronic_conditions, 'Diabetes')
    
    def test_medical_record_str_representation(self):
        """Test la representación string del modelo"""
        record = MedicalRecord.objects.create(patient=self.patient)
        expected = "Historia Clínica de Juan Pérez - DNI: 12345678"
        self.assertEqual(str(record), expected)
    
    def test_medical_record_one_to_one_with_patient(self):
        """Test que cada paciente tiene solo una historia clínica"""
        MedicalRecord.objects.create(patient=self.patient)
        
        with self.assertRaises(IntegrityError):
            MedicalRecord.objects.create(patient=self.patient)


class UserProfileModelTest(TestCase):
    """Tests para el modelo UserProfile"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_user_profile(self):
        """Test crear un perfil de usuario correctamente"""
        profile = UserProfile.objects.create(
            user=self.user,
            role='DOCTOR',
            phone='+54911234567'
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.role, 'DOCTOR')
        self.assertTrue(profile.is_active)
    
    def test_user_profile_str_representation(self):
        """Test la representación string del modelo"""
        profile = UserProfile.objects.create(
            user=self.user,
            role='DOCTOR',
            phone='+54911234567'
        )
        expected = f"{self.user.get_full_name()} - Médico"
        self.assertEqual(str(profile), expected)
    
    def test_user_profile_one_to_one_with_user(self):
        """Test que cada usuario tiene solo un perfil"""
        UserProfile.objects.create(
            user=self.user,
            role='DOCTOR',
            phone='+54911234567'
        )
        
        with self.assertRaises(IntegrityError):
            UserProfile.objects.create(
                user=self.user,
                role='PATIENT',
                phone='+54911234568'
            )


class AuditLogModelTest(TestCase):
    """Tests para el modelo AuditLog"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_audit_log(self):
        """Test crear un log de auditoría correctamente"""
        log = AuditLog.objects.create(
            user=self.user,
            action='CREATE',
            model_name='Person',
            object_id='123',
            description='Paciente creado',
            ip_address='127.0.0.1'
        )
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.action, 'CREATE')
        self.assertEqual(log.model_name, 'Person')
        self.assertEqual(log.object_id, '123')
    
    def test_audit_log_str_representation(self):
        """Test la representación string del modelo"""
        log = AuditLog.objects.create(
            user=self.user,
            action='CREATE',
            model_name='Person',
            object_id='123',
            description='Paciente creado'
        )
        expected_start = f"{self.user} - Crear - Person"
        self.assertTrue(str(log).startswith(expected_start))
    
    def test_audit_log_ordering(self):
        """Test que los logs se ordenan por fecha descendente"""
        from django.utils import timezone
        import time
        
        # Crear primer log
        log1 = AuditLog.objects.create(
            user=self.user,
            action='CREATE',
            model_name='Person',
            description='Primer log'
        )
        
        # Esperar un poco para asegurar diferencia de tiempo
        time.sleep(0.01)
        
        # Crear segundo log
        log2 = AuditLog.objects.create(
            user=self.user,
            action='UPDATE',
            model_name='Person',
            description='Segundo log'
        )
        
        logs = AuditLog.objects.all()
        self.assertEqual(logs[0], log2)  # Más reciente primero
        self.assertEqual(logs[1], log1)
