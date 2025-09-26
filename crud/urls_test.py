"""
URL configuration for testing.
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from history import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('api/dashboard-data/', views.dashboard_data_api, name='dashboard_data_api'),
    
    # Pacientes
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/create/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    path('patients/<int:patient_pk>/medical-record/', views.medical_record_edit, name='medical_record_edit'),
    
    # Consultas
    path('consults/', views.consult_list, name='consult_list'),
    path('consults/<int:pk>/', views.consult_detail, name='consult_detail'),
    path('consults/create/', views.consult_create, name='consult_create'),
    
    # Doctores
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/create/', views.doctor_create, name='doctor_create'),
]

# Servir archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

