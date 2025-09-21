import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from faker import Faker
from ..models import Person, Doctor, Consult, Diagnosis, Treatment, MedicalRecord

fake = Faker('es_ES')  # Usar datos en español

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f"user{n}")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    is_active = True

class PersonFactory(DjangoModelFactory):
    class Meta:
        model = Person
    
    name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    dni = factory.Sequence(lambda n: f"{fake.random_int(min=1000000, max=99999999)}")
    birth_date = factory.Faker('date_of_birth', minimum_age=18, maximum_age=80)
    gender = factory.Iterator(['M', 'F', 'O'])
    phone = factory.Faker('phone_number')
    email = factory.Faker('email')
    address = factory.Faker('address')
    observations = factory.Faker('text', max_nb_chars=200)
    is_active = True

class DoctorFactory(DjangoModelFactory):
    class Meta:
        model = Doctor
    
    user = factory.SubFactory(UserFactory)
    license_number = factory.Sequence(lambda n: f"DR{n:06d}")
    specialty = factory.Iterator(['GP', 'CARD', 'DERM', 'NEURO', 'PED', 'GYN', 'ORTH', 'PSYCH', 'OTHER'])
    phone = factory.Faker('phone_number')
    is_active = True

class ConsultFactory(DjangoModelFactory):
    class Meta:
        model = Consult
    
    patient = factory.SubFactory(PersonFactory)
    doctor = factory.SubFactory(DoctorFactory)
    date = factory.Faker('date_time_between', start_date='-1y', end_date='now')
    consult_type = factory.Iterator(['FIRST', 'FOLLOW', 'EMERGENCY', 'ROUTINE'])
    reason = factory.Faker('text', max_nb_chars=300)
    symptoms = factory.Faker('text', max_nb_chars=500)
    vital_signs = factory.Faker('text', max_nb_chars=200)

class DiagnosisFactory(DjangoModelFactory):
    class Meta:
        model = Diagnosis
    
    consult = factory.SubFactory(ConsultFactory)
    description = factory.Faker('text', max_nb_chars=500)
    icd_code = factory.Faker('bothify', text='?##.##')

class TreatmentFactory(DjangoModelFactory):
    class Meta:
        model = Treatment
    
    consult = factory.SubFactory(ConsultFactory)
    description = factory.Faker('text', max_nb_chars=500)
    medications = factory.Faker('text', max_nb_chars=300)
    instructions = factory.Faker('text', max_nb_chars=400)
    follow_up_date = factory.Faker('future_date', end_date='+30d')

class MedicalRecordFactory(DjangoModelFactory):
    class Meta:
        model = MedicalRecord
    
    patient = factory.SubFactory(PersonFactory)
    allergies = factory.Faker('text', max_nb_chars=200)
    chronic_conditions = factory.Faker('text', max_nb_chars=300)
    family_history = factory.Faker('text', max_nb_chars=400)
    social_history = factory.Faker('text', max_nb_chars=300)
