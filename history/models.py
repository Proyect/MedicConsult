from django.db import models

class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    last_name = models.TextField()
    dni = models.TextField()
    birth_date = models.DateField()
    gender = models.enums() # F M X
    phone = models.PhoneNumberField()
    email = models.EmailField()
    address = models.TextField()
    observations = models.TextField()

    def __str__(self) -> str:
        return f"Persona:  {self.name} {self.last_name} {self.dni}"

class Dr(models.Model, Person):
    id = models.AutoField(primary_key=True)
    idPerson = models.ForeignKey(Person.id)
    status = models.enums()
    
    def __str__(self) -> str:
        return super().__str__()
    
class Consult(models.Model, Person, Dr):
    id = models.AutoField(primary_key=True)
    idPerson = models.ForeignKey(Person.id)
    idDr = models.ForeignKey(Dr.id)
    date = models.DateField()
    
    def __str__(self) -> str:
        return super().__str__()
    
class Diagnosis(models.Model):
    id = models.AutoField(primary_key=True)
    consult = models.OneToOneField(Consult)
    description = models.TextField()
    
    def __str__(self) -> str:
        return super().__str__()
    
class Treatment(models.Model):
    id = models.AutoField(primary_key=True)
    consult = models.OneToOneField(Consult)
    description = models.TextField()
    
    def __str__(self) -> str:
        return super().__str__()
    
