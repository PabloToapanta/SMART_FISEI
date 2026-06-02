from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import NodoJerarquico, Documento
from .forms import NodoJerarquicoForm, DocumentoForm
from .services import ArbolNario, NodoArbol
from historial.utils import registrar_accion

def inicializar_jerarquia_base():
    if NodoJerarquico.objects.count() > 0:
        return

    # RAÍZ: FISEI
    fisei = NodoJerarquico.objects.create(nombre="FISEI — Facultad de Ingeniería en Sistemas, Electrónica e Industrial", tipo='facultad')

    # 1. Secretaría General
    sec_gen = NodoJerarquico.objects.create(nombre="Secretaría General", tipo='departamento', padre=fisei)
    
    reg_norm = NodoJerarquico.objects.create(nombre="Reglamentos y Normativas", tipo='area', padre=sec_gen)
    for doc in ["reglamento_interno_fisei.pdf", "reglamento_evaluacion_calificaciones.pdf", "reglamento_practicas_preprofesionales.pdf", "codigo_etica_estudiantes.pdf"]:
        Documento.objects.create(nombre=doc, nodo=reg_norm)

    forms_ofic = NodoJerarquico.objects.create(nombre="Formularios Oficiales", tipo='area', padre=sec_gen)
    for doc in ["formulario_matricula.docx", "formulario_retiro_materia.docx", "formulario_homologacion.docx", "formulario_segunda_matricula.docx", "formulario_revision_examen.docx"]:
        Documento.objects.create(nombre=doc, nodo=forms_ofic)

    cal_res = NodoJerarquico.objects.create(nombre="Calendarios y Resoluciones", tipo='area', padre=sec_gen)
    for doc in ["calendario_academico_2025_2026.pdf", "resolucion_consejo_directivo_001.pdf", "resolucion_consejo_directivo_002.pdf"]:
        Documento.objects.create(nombre=doc, nodo=cal_res)

    com_inst = NodoJerarquico.objects.create(nombre="Comunicados Institucionales", tipo='area', padre=sec_gen)
    for doc in ["comunicado_inicio_semestre.pdf", "comunicado_proceso_titulacion.pdf"]:
        Documento.objects.create(nombre=doc, nodo=com_inst)

    # 2. Dirección Académica
    dir_acad = NodoJerarquico.objects.create(nombre="Dirección Académica", tipo='departamento', padre=fisei)
    
    dist_doc = NodoJerarquico.objects.create(nombre="Distributivos Docentes", tipo='area', padre=dir_acad)
    for doc in ["distributivo_software_2025_2026.pdf", "distributivo_electronica_2025_2026.pdf"]:
        Documento.objects.create(nombre=doc, nodo=dist_doc)
    
    mallas = NodoJerarquico.objects.create(nombre="Mallas Curriculares", tipo='area', padre=dir_acad)
    for doc in ["malla_software_v2023.pdf", "malla_tics_v2023.pdf", "malla_robotica_v2023.pdf", "malla_industrial_v2023.pdf", "malla_telecomunicaciones_v2023.pdf"]:
        Documento.objects.create(nombre=doc, nodo=mallas)
    
    plan_acad = NodoJerarquico.objects.create(nombre="Planificación Académica", tipo='area', padre=dir_acad)
    for doc in ["plan_contingencia_academica.pdf", "cronograma_examenes_2026.pdf"]:
        Documento.objects.create(nombre=doc, nodo=plan_acad)

    # 3. Bienestar Estudiantil
    bienestar = NodoJerarquico.objects.create(nombre="Bienestar Estudiantil", tipo='departamento', padre=fisei)
    for doc in ["becas_y_ayudas_economicas.pdf", "reglamento_becas_fisei.pdf", "servicios_psicologia.pdf", "programa_tutoria_academica.pdf"]:
        Documento.objects.create(nombre=doc, nodo=bienestar)

    # 4. Carreras
    # Software
    sw = NodoJerarquico.objects.create(nombre="Carrera de Ingeniería en Software", tipo='carrera', padre=fisei)
    n = NodoJerarquico.objects.create(nombre="Información General", tipo='area', padre=sw)
    Documento.objects.create(nombre="perfil_egreso_software.pdf", nodo=n)
    Documento.objects.create(nombre="plan_estudios_software.pdf", nodo=n)
    
    n = NodoJerarquico.objects.create(nombre="Primer Semestre", tipo='area', padre=sw)
    Documento.objects.create(nombre="silabo_fundamentos_programacion.pdf", nodo=n)
    Documento.objects.create(nombre="silabo_matematica_discreta.pdf", nodo=n)
    
    n = NodoJerarquico.objects.create(nombre="Segundo Semestre", tipo='area', padre=sw)
    Documento.objects.create(nombre="silabo_estructura_datos.pdf", nodo=n)
    Documento.objects.create(nombre="silabo_calculo.pdf", nodo=n)
    
    n = NodoJerarquico.objects.create(nombre="Tercer Semestre", tipo='area', padre=sw)
    Documento.objects.create(nombre="silabo_bases_datos.pdf", nodo=n)
    Documento.objects.create(nombre="silabo_algoritmos.pdf", nodo=n)
    
    n = NodoJerarquico.objects.create(nombre="Prácticas Preprofesionales", tipo='area', padre=sw)
    Documento.objects.create(nombre="guia_practicas_software.pdf", nodo=n)
    Documento.objects.create(nombre="formato_informe_practicas.docx", nodo=n)
    
    n = NodoJerarquico.objects.create(nombre="Titulación", tipo='area', padre=sw)
    Documento.objects.create(nombre="guia_trabajo_titulacion_software.pdf", nodo=n)
    Documento.objects.create(nombre="formato_proyecto_titulacion.docx", nodo=n)

    # TICs
    tics = NodoJerarquico.objects.create(nombre="Carrera de TICs", tipo='carrera', padre=fisei)
    n = NodoJerarquico.objects.create(nombre="Información General", tipo='area', padre=tics)
    Documento.objects.create(nombre="perfil_egreso_tics.pdf", nodo=n)
    Documento.objects.create(nombre="plan_estudios_tics.pdf", nodo=n)
    n = NodoJerarquico.objects.create(nombre="Primer Semestre", tipo='area', padre=tics)
    Documento.objects.create(nombre="silabo_introduccion_tics.pdf", nodo=n)
    n = NodoJerarquico.objects.create(nombre="Redes y Comunicaciones", tipo='area', padre=tics)
    Documento.objects.create(nombre="silabo_redes_computadoras.pdf", nodo=n)
    Documento.objects.create(nombre="silabo_seguridad_informatica.pdf", nodo=n)
    n = NodoJerarquico.objects.create(nombre="Prácticas Preprofesionales", tipo='area', padre=tics)
    Documento.objects.create(nombre="guia_practicas_tics.pdf", nodo=n)
    n = NodoJerarquico.objects.create(nombre="Titulación", tipo='area', padre=tics)
    Documento.objects.create(nombre="guia_trabajo_titulacion_tics.pdf", nodo=n)

    # Robótica
    rob = NodoJerarquico.objects.create(nombre="Carrera de Robótica e Inteligencia Artificial", tipo='carrera', padre=fisei)
    n = NodoJerarquico.objects.create(nombre="Información General", tipo='area', padre=rob)
    Documento.objects.create(nombre="perfil_egreso_robotica.pdf", nodo=n)
    Documento.objects.create(nombre="plan_estudios_robotica.pdf", nodo=n)
    n = NodoJerarquico.objects.create(nombre="Electrónica y Control", tipo='area', padre=rob)
    Documento.objects.create(nombre="silabo_electronica_basica.pdf", nodo=n)
    Documento.objects.create(nombre="silabo_control_automatico.pdf", nodo=n)
    n = NodoJerarquico.objects.create(nombre="Inteligencia Artificial", tipo='area', padre=rob)
    Documento.objects.create(nombre="silabo_machine_learning.pdf", nodo=n)
    Documento.objects.create(nombre="silabo_vision_computacional.pdf", nodo=n)
    n = NodoJerarquico.objects.create(nombre="Prácticas Preprofesionales", tipo='area', padre=rob)
    Documento.objects.create(nombre="guia_practicas_robotica.pdf", nodo=n)
    n = NodoJerarquico.objects.create(nombre="Titulación", tipo='area', padre=rob)
    Documento.objects.create(nombre="guia_trabajo_titulacion_robotica.pdf", nodo=n)

    # Industrial
    ind = NodoJerarquico.objects.create(nombre="Carrera de Ingeniería Industrial", tipo='carrera', padre=fisei)
    n = NodoJerarquico.objects.create(nombre="Información General", tipo='area', padre=ind)
    Documento.objects.create(nombre="perfil_egreso_industrial.pdf", nodo=n)
    Documento.objects.create(nombre="plan_estudios_industrial.pdf", nodo=n)
    n = NodoJerarquico.objects.create(nombre="Gestión y Procesos", tipo='area', padre=ind)
    Documento.objects.create(nombre="silabo_gestion_calidad.pdf", nodo=n)
    Documento.objects.create(nombre="silabo_investigacion_operaciones.pdf", nodo=n)
    n = NodoJerarquico.objects.create(nombre="Seguridad Industrial", tipo='area', padre=ind)
    Documento.objects.create(nombre="silabo_seguridad_trabajo.pdf", nodo=n)
    Documento.objects.create(nombre="reglamento_seguridad_laboratorios.pdf", nodo=n)
    n = NodoJerarquico.objects.create(nombre="Prácticas Preprofesionales", tipo='area', padre=ind)
    Documento.objects.create(nombre="guia_practicas_industrial.pdf", nodo=n)
    n = NodoJerarquico.objects.create(nombre="Titulación", tipo='area', padre=ind)
    Documento.objects.create(nombre="guia_trabajo_titulacion_industrial.pdf", nodo=n)

    # Telecomunicaciones
    tel = NodoJerarquico.objects.create(nombre="Carrera de Telecomunicaciones", tipo='carrera', padre=fisei)
    n = NodoJerarquico.objects.create(nombre="Información General", tipo='area', padre=tel)
    Documento.objects.create(nombre="perfil_egreso_telecomunicaciones.pdf", nodo=n)
    Documento.objects.create(nombre="plan_estudios_telecomunicaciones.pdf", nodo=n)
    n = NodoJerarquico.objects.create(nombre="Sistemas de Transmisión", tipo='area', padre=tel)
    Documento.objects.create(nombre="silabo_comunicaciones_digitales.pdf", nodo=n)
    Documento.objects.create(nombre="silabo_antenas_propagacion.pdf", nodo=n)
    n = NodoJerarquico.objects.create(nombre="Prácticas Preprofesionales", tipo='area', padre=tel)
    Documento.objects.create(nombre="guia_practicas_telecomunicaciones.pdf", nodo=n)
    n = NodoJerarquico.objects.create(nombre="Titulación", tipo='area', padre=tel)
    Documento.objects.create(nombre="guia_trabajo_titulacion_telecomunicaciones.pdf", nodo=n)

    # 5. Club de Robótica
    club = NodoJerarquico.objects.create(nombre="Club de Robótica FISEI", tipo='departamento', padre=fisei)
    for doc in ["reglamento_club_robotica.pdf", "convocatoria_miembros_2026.pdf", "proyectos_activos_2026.pdf", "resultados_competencias_2025.pdf"]:
        Documento.objects.create(nombre=doc, nodo=club)

    # 6. CTT
    ctt = NodoJerarquico.objects.create(nombre="CTT — Centro de Transferencia de Tecnología", tipo='departamento', padre=fisei)
    inf = NodoJerarquico.objects.create(nombre="Información General", tipo='area', padre=ctt)
    Documento.objects.create(nombre="oferta_talleres_ctt_2026.pdf", nodo=inf)
    Documento.objects.create(nombre="reglamento_uso_ctt.pdf", nodo=inf)
    
    tall = NodoJerarquico.objects.create(nombre="Talleres de Capacitación", tipo='area', padre=ctt)
    for doc in ["taller_arduino_basico.pdf", "taller_raspberry_pi.pdf", "taller_impresion_3d.pdf", "taller_soldadura_electronica.pdf", "taller_automatizacion_industrial.pdf"]:
        Documento.objects.create(nombre=doc, nodo=tall)
    
    cert = NodoJerarquico.objects.create(nombre="Certificaciones", tipo='area', padre=ctt)
    Documento.objects.create(nombre="formato_certificado_taller.docx", nodo=cert)
    Documento.objects.create(nombre="cronograma_talleres_2026.pdf", nodo=cert)

@login_required
def consultar_documento_view(request, doc_id):
    documento = get_object_or_404(Documento, id=doc_id)
    registrar_accion(request.user, 'documentos', 'Documento consultado', f'{documento.nombre}')
    messages.info(request, f"Has consultado el documento: {documento.nombre}")
    return redirect('documentos:jerarquia')

@login_required
def jerarquia_view(request):
    inicializar_jerarquia_base()
    nodos = NodoJerarquico.objects.all()
    arbol = ArbolNario(None)
    raiz = arbol.construir_desde_db(nodos)
    
    query = request.GET.get('q')
    resultados_busqueda = []
    if query:
        # Req 4: Búsqueda usando recorrido DFS del Árbol N-ario
        def buscar_en_arbol(nodo_arbol, texto):
            res = []
            nodo_obj = nodo_arbol.dato
            # Buscar en el nombre del nodo
            if texto.lower() in nodo_obj.nombre.lower():
                res.append({'tipo': 'Nodo', 'obj': nodo_obj})
            # Buscar en los documentos del nodo
            for doc in nodo_obj.documentos.all():
                if texto.lower() in doc.nombre.lower():
                    res.append({'tipo': 'Documento', 'obj': doc, 'ruta': nodo_obj.nombre})
            # Recurrir en hijos (N-ario)
            for hijo in nodo_arbol.hijos:
                res.extend(buscar_en_arbol(hijo, texto))
            return res
        
        if raiz:
            resultados_busqueda = buscar_en_arbol(raiz, query)

    return render(request, 'documentos/jerarquia.html', {
        'raiz': raiz,
        'resultados': resultados_busqueda,
        'query': query
    })

@login_required
def gestionar_nodo_view(request, nodo_id=None):
    if request.user.rol != 'admin':
        return redirect('documentos:jerarquia')
    
    nodo = get_object_or_404(NodoJerarquico, id=nodo_id) if nodo_id else None
    if request.method == 'POST':
        form = NodoJerarquicoForm(request.POST, instance=nodo)
        if form.is_valid():
            form.save()
            messages.success(request, "Estructura institucional actualizada.")
            return redirect('documentos:jerarquia')
    else:
        form = NodoJerarquicoForm(instance=nodo)
    
    return render(request, 'documentos/nodo_form.html', {'form': form, 'nodo': nodo})

@login_required
def eliminar_nodo_view(request, nodo_id):
    if request.user.rol != 'admin':
        return redirect('documentos:jerarquia')
    nodo = get_object_or_404(NodoJerarquico, id=nodo_id)
    nodo.delete()
    messages.success(request, "Nodo eliminado de la jerarquía.")
    return redirect('documentos:jerarquia')

@login_required
def subir_documento_view(request):
    if request.user.rol not in ['admin', 'administrativo']:
        return redirect('documentos:jerarquia')
    
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.subido_por = request.user
            doc.save()
            messages.success(request, f"Documento '{doc.nombre}' asociado exitosamente.")
            return redirect('documentos:jerarquia')
    else:
        form = DocumentoForm()
    
    return render(request, 'documentos/documento_form.html', {'form': form})
