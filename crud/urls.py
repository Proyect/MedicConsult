"""
URL configuration for crud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from history import views
from history import report_views

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
    
    # Reportes
    path('reports/', report_views.reports_dashboard, name='reports_dashboard'),
    path('reports/patients/', report_views.generate_patients_report, name='generate_patients_report'),
    path('reports/consults/', report_views.generate_consults_report, name='generate_consults_report'),
    path('reports/statistics/', report_views.generate_statistics_report, name='generate_statistics_report'),
    path('reports/list/', report_views.reports_list, name='reports_list'),
    path('reports/<int:report_id>/delete/', report_views.delete_report, name='delete_report'),
    
    # API
    path('api/dashboard-data/', report_views.dashboard_data_api, name='dashboard_data_api'),
]

# Servir archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
