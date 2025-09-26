import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from history.models import Person, Doctor, Consult, UserProfile
from datetime import date, datetime


@pytest.fixture
def admin_user():
    """Fixture para usuario administrador"""
    return User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='testpass123',
        is_staff=True,
        is_superuser=True
    )


@pytest.fixture
def doctor_user():
    """Fixture para usuario doctor"""
    return User.objects.create_user(
        username='doctor',
        email='doctor@example.com',
        password='testpass123',
        first_name='Dr. Juan',
        last_name='Médico'
    )


@pytest.fixture
def doctor(doctor_user):
    """Fixture para doctor"""
    return Doctor.objects.create(
        user=doctor_user,
        license_number='MP12345',
        specialty='GP',
        phone='+54911234567'
    )


@pytest.fixture
def patient():
    """Fixture para paciente"""
    return Person.objects.create(
        name='Juan',
        last_name='Pérez',
        dni='12345678',
        birth_date=date(1990, 1, 1),
        gender='M',
        phone='+54911234567',
        email='juan.perez@example.com',
        address='Calle 123, Ciudad'
    )


@pytest.fixture
def consult(patient, doctor):
    """Fixture para consulta"""
    return Consult.objects.create(
        patient=patient,
        doctor=doctor,
        date=datetime.now(),
        consult_type='FIRST',
        reason='Dolor de cabeza',
        symptoms='Cefalea intensa',
        vital_signs='TA: 120/80'
    )


@pytest.fixture
def patient_profile():
    """Fixture para perfil de paciente"""
    user = User.objects.create_user(
        username='patient',
        email='patient@example.com',
        password='testpass123'
    )
    return UserProfile.objects.create(
        user=user,
        role='PATIENT',
        phone='+54911234568'
    )

