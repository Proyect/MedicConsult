from django.contrib import admin
from .models import Person, Dr, Consult, Diagnosis, Treatment 

admin.site.register(Person)
admin.site.register(Dr)
admin.site.register(Consult)
admin.site.register(Diagnosis)
admin.site.register(Treatment)

