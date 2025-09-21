from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Person, Doctor, Consult, Diagnosis, Treatment, MedicalRecord

class DoctorInline(admin.StackedInline):
    model = Doctor
    can_delete = False
    verbose_name_plural = 'Perfil de Doctor'

class CustomUserAdmin(UserAdmin):
    inlines = (DoctorInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'dni', 'email', 'phone', 'age', 'is_active')
    list_filter = ('gender', 'is_active', 'created_at')
    search_fields = ('name', 'last_name', 'dni', 'email')
    readonly_fields = ('created_at', 'updated_at', 'age')
    fieldsets = (
        ('Información Personal', {
            'fields': ('name', 'last_name', 'dni', 'birth_date', 'gender', 'age')
        }),
        ('Contacto', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Información Adicional', {
            'fields': ('observations', 'is_active')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'specialty', 'phone', 'is_active')
    list_filter = ('specialty', 'is_active', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'license_number')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Consult)
class ConsultAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'date', 'consult_type', 'created_at')
    list_filter = ('consult_type', 'date', 'created_at')
    search_fields = ('patient__name', 'patient__last_name', 'doctor__user__first_name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('consult', 'icd_code', 'created_at')
    search_fields = ('consult__patient__name', 'consult__patient__last_name', 'icd_code')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('consult', 'follow_up_date', 'created_at')
    search_fields = ('consult__patient__name', 'consult__patient__last_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'created_at', 'updated_at')
    search_fields = ('patient__name', 'patient__last_name')
    readonly_fields = ('created_at', 'updated_at')

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

