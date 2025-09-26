"""
Vistas para reportes y dashboard
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Person, Doctor, Consult, Report, AuditLog
from .reports import ReportGenerator, get_statistics_data
from .utils import get_user_role, require_role
import json

@login_required
@require_role('administrator')
def reports_dashboard(request):
    """Dashboard principal de reportes"""
    context = {
        'user_role': get_user_role(request.user),
        'recent_reports': Report.objects.filter(created_by=request.user).order_by('-created_at')[:5],
        'total_reports': Report.objects.filter(created_by=request.user).count(),
    }
    return render(request, 'reports/dashboard.html', context)

@login_required
@require_role('administrator')
def generate_patients_report(request):
    """Generar reporte de pacientes"""
    if request.method == 'POST':
        form_data = request.POST
        
        # Aplicar filtros
        patients = Person.objects.filter(is_active=True)
        
        # Filtro por nombre/apellido/DNI
        search = form_data.get('search', '')
        if search:
            patients = patients.filter(
                Q(name__icontains=search) | 
                Q(last_name__icontains=search) | 
                Q(dni__icontains=search)
            )
        
        # Filtro por género
        gender = form_data.get('gender', '')
        if gender:
            patients = patients.filter(gender=gender)
        
        # Filtro por rango de edad
        min_age = form_data.get('min_age', '')
        max_age = form_data.get('max_age', '')
        
        if min_age:
            max_birth_date = timezone.now().date() - timedelta(days=int(min_age) * 365)
            patients = patients.filter(birth_date__lte=max_birth_date)
        
        if max_age:
            min_birth_date = timezone.now().date() - timedelta(days=int(max_age) * 365)
            patients = patients.filter(birth_date__gte=min_birth_date)
        
        # Generar reporte
        report_type = form_data.get('format', 'pdf')
        title = f"Reporte de Pacientes - {datetime.now().strftime('%d/%m/%Y')}"
        
        # Guardar reporte en base de datos
        report = Report.objects.create(
            name=title,
            report_type='PATIENTS',
            description=f"Reporte generado con {patients.count()} pacientes",
            filters=form_data.dict(),
            created_by=request.user
        )
        
        generator = ReportGenerator()
        
        if report_type == 'pdf':
            buffer = generator.generate_patients_pdf(patients, title)
            response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="reporte_pacientes_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
            
            # Actualizar ruta del archivo
            report.file_path = f"reports/patients_{report.id}.pdf"
            report.save()
            
        else:  # Excel
            wb = generator.generate_patients_excel(patients, title)
            response = HttpResponse(
                wb.save,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="reporte_pacientes_{datetime.now().strftime("%Y%m%d_%H%M")}.xlsx"'
            
            # Actualizar ruta del archivo
            report.file_path = f"reports/patients_{report.id}.xlsx"
            report.save()
        
        # Log de auditoría
        AuditLog.objects.create(
            user=request.user,
            action='CREATE',
            model_name='Report',
            object_id=str(report.id),
            description=f'Generó reporte de pacientes: {title}',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        
        return response
    
    context = {
        'user_role': get_user_role(request.user),
        'genders': Person.GENDER_CHOICES,
    }
    return render(request, 'reports/patients_form.html', context)

@login_required
@require_role('administrator')
def generate_consults_report(request):
    """Generar reporte de consultas"""
    if request.method == 'POST':
        form_data = request.POST
        
        # Aplicar filtros
        consults = Consult.objects.all()
        
        # Filtro por doctor
        doctor_id = form_data.get('doctor', '')
        if doctor_id:
            consults = consults.filter(doctor_id=doctor_id)
        
        # Filtro por tipo de consulta
        consult_type = form_data.get('consult_type', '')
        if consult_type:
            consults = consults.filter(consult_type=consult_type)
        
        # Filtro por rango de fechas
        start_date = form_data.get('start_date', '')
        end_date = form_data.get('end_date', '')
        
        if start_date:
            consults = consults.filter(date__gte=start_date)
        
        if end_date:
            consults = consults.filter(date__lte=end_date)
        
        # Generar reporte
        report_type = form_data.get('format', 'pdf')
        title = f"Reporte de Consultas - {datetime.now().strftime('%d/%m/%Y')}"
        
        # Guardar reporte en base de datos
        report = Report.objects.create(
            name=title,
            report_type='CONSULTS',
            description=f"Reporte generado con {consults.count()} consultas",
            filters=form_data.dict(),
            created_by=request.user
        )
        
        generator = ReportGenerator()
        
        if report_type == 'pdf':
            buffer = generator.generate_consults_pdf(consults, title)
            response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="reporte_consultas_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
            
            report.file_path = f"reports/consults_{report.id}.pdf"
            report.save()
            
        else:  # Excel
            wb = generator.generate_consults_excel(consults, title)
            response = HttpResponse(
                wb.save,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="reporte_consultas_{datetime.now().strftime("%Y%m%d_%H%M")}.xlsx"'
            
            report.file_path = f"reports/consults_{report.id}.xlsx"
            report.save()
        
        # Log de auditoría
        AuditLog.objects.create(
            user=request.user,
            action='CREATE',
            model_name='Report',
            object_id=str(report.id),
            description=f'Generó reporte de consultas: {title}',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        
        return response
    
    context = {
        'user_role': get_user_role(request.user),
        'doctors': Doctor.objects.filter(is_active=True),
        'consult_types': Consult.CONSULT_TYPE_CHOICES,
    }
    return render(request, 'reports/consults_form.html', context)

@login_required
@require_role('administrator')
def generate_statistics_report(request):
    """Generar reporte de estadísticas"""
    if request.method == 'POST':
        form_data = request.POST
        
        report_type = form_data.get('format', 'pdf')
        title = f"Estadísticas Generales - {datetime.now().strftime('%d/%m/%Y')}"
        
        # Guardar reporte en base de datos
        report = Report.objects.create(
            name=title,
            report_type='STATISTICS',
            description="Reporte de estadísticas generales del sistema",
            filters=form_data.dict(),
            created_by=request.user
        )
        
        generator = ReportGenerator()
        
        if report_type == 'pdf':
            buffer = generator.generate_statistics_pdf(title)
            response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="estadisticas_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
            
            report.file_path = f"reports/statistics_{report.id}.pdf"
            report.save()
            
        else:  # Excel - Para estadísticas, generamos un Excel con múltiples hojas
            wb = openpyxl.Workbook()
            
            # Hoja 1: Resumen general
            ws1 = wb.active
            ws1.title = "Resumen General"
            
            stats_data = get_statistics_data()
            
            ws1['A1'] = "Estadísticas Generales"
            ws1['A1'].font = openpyxl.styles.Font(bold=True, size=16)
            
            ws1['A3'] = "Total de Pacientes"
            ws1['B3'] = stats_data['total_patients']
            ws1['A4'] = "Total de Doctores"
            ws1['B4'] = stats_data['total_doctors']
            ws1['A5'] = "Total de Consultas"
            ws1['B5'] = stats_data['total_consults']
            ws1['A6'] = "Consultas este mes"
            ws1['B6'] = stats_data['consults_this_month']
            
            # Hoja 2: Consultas por tipo
            ws2 = wb.create_sheet("Consultas por Tipo")
            ws2['A1'] = "Tipo de Consulta"
            ws2['B1'] = "Cantidad"
            
            row = 2
            for item in stats_data['consults_by_type']:
                consult_type_display = dict(Consult.CONSULT_TYPE_CHOICES).get(item['consult_type'], item['consult_type'])
                ws2[f'A{row}'] = consult_type_display
                ws2[f'B{row}'] = item['count']
                row += 1
            
            # Hoja 3: Pacientes por género
            ws3 = wb.create_sheet("Pacientes por Género")
            ws3['A1'] = "Género"
            ws3['B1'] = "Cantidad"
            
            row = 2
            for item in stats_data['patients_by_gender']:
                gender_display = dict(Person.GENDER_CHOICES).get(item['gender'], item['gender'])
                ws3[f'A{row}'] = gender_display
                ws3[f'B{row}'] = item['count']
                row += 1
            
            response = HttpResponse(
                wb.save,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="estadisticas_{datetime.now().strftime("%Y%m%d_%H%M")}.xlsx"'
            
            report.file_path = f"reports/statistics_{report.id}.xlsx"
            report.save()
        
        # Log de auditoría
        AuditLog.objects.create(
            user=request.user,
            action='CREATE',
            model_name='Report',
            object_id=str(report.id),
            description=f'Generó reporte de estadísticas: {title}',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        
        return response
    
    context = {
        'user_role': get_user_role(request.user),
    }
    return render(request, 'reports/statistics_form.html', context)

@login_required
@require_role('administrator')
def reports_list(request):
    """Lista de reportes generados"""
    reports = Report.objects.filter(created_by=request.user).order_by('-created_at')
    
    context = {
        'reports': reports,
        'user_role': get_user_role(request.user),
    }
    return render(request, 'reports/list.html', context)

@login_required
@require_role('administrator')
def delete_report(request, report_id):
    """Eliminar reporte"""
    try:
        report = Report.objects.get(id=report_id, created_by=request.user)
        report.delete()
        messages.success(request, 'Reporte eliminado exitosamente')
    except Report.DoesNotExist:
        messages.error(request, 'Reporte no encontrado')
    
    return redirect('reports_list')

@login_required
def dashboard_data_api(request):
    """API para obtener datos del dashboard"""
    if request.method == 'GET':
        data = get_statistics_data()
        return JsonResponse(data)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

