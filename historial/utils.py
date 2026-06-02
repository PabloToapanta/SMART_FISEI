from .models import HistorialAccion
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from datetime import datetime

def registrar_accion(usuario, modulo, accion, detalle=''):
    """Registra una acción importante en la base de datos."""
    HistorialAccion.objects.create(
        usuario=usuario, 
        modulo=modulo, 
        accion=accion, 
        detalle=detalle
    )

def generar_pdf_reporte(titulo, encabezados, datos, filename):
    """Genera un archivo PDF a partir de una lista de encabezados y datos."""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    header_style = styles['Normal']

    # Título y Fecha
    elements.append(Paragraph(titulo, title_style))
    elements.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", header_style))
    elements.append(Spacer(1, 20))

    # Crear Tabla
    table_data = [encabezados] + datos
    t = Table(table_data, repeatRows=1)
    
    # Estilo de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#C0392B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    t.setStyle(style)
    elements.append(t)

    doc.build(elements)
    return response
