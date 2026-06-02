from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from usuarios.models import Usuario
from turnos.models import Turno, Ventanilla
from tramites.models import Tramite, TipoTramite, HistorialEstadoTramite
from documentos.models import NodoJerarquico, Documento
from rutas.models import EspacioFisico, ConexionEspacio
from historial.models import HistorialAccion
from historial.utils import registrar_accion
from turnos.services import ColaFIFO, ListaCircular
from historial.services import PilaHistorial, ListaDoble as HistorialListaDoble
from tramites.services import ListaSecuencial, ListaDoble as TramiteListaDoble
from documentos.services import ArbolNario, NodoArbol
from rutas.services import Grafo

class AutenticacionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_password = 'Admin2026#'
        self.estudiante = Usuario.objects.create_user(
            username='estudiante', email='estudiante@uta.edu.ec', 
            password=self.user_password, rol='estudiante'
        )
        self.admin = Usuario.objects.create_superuser(
            username='admin', email='admin@uta.edu.ec', 
            password=self.user_password, rol='admin'
        )

    def test_login_exitoso(self):
        response = self.client.post(reverse('login'), {
            'username': 'estudiante@uta.edu.ec',
            'password': self.user_password
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_fallido(self):
        response = self.client.post(reverse('login'), {
            'username': 'estudiante@uta.edu.ec',
            'password': 'WrongPassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_redireccion_sin_login(self):
        urls = [reverse('estado_cola'), reverse('mis_tramites'), reverse('historial:historial')]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn('/login/', response.url)

    def test_acceso_admin_bloqueado_a_estudiante(self):
        self.client.login(username='estudiante@uta.edu.ec', password=self.user_password)
        response = self.client.get(reverse('historial:reportes'))
        self.assertEqual(response.status_code, 403)

class TurnosTests(TestCase):
    def setUp(self):
        self.user_password = 'Admin2026#'
        self.estudiante = Usuario.objects.create_user(
            username='ana', email='ana@uta.edu.ec', password=self.user_password, rol='estudiante'
        )
        self.admin_atencion = Usuario.objects.create_user(
            username='maria', email='maria@uta.edu.ec', password=self.user_password, rol='administrativo'
        )
        self.ventanilla = Ventanilla.objects.create(nombre="Ventanilla 1", responsable=self.admin_atencion)

    def test_solicitar_turno(self):
        self.client.login(username='ana@uta.edu.ec', password=self.user_password)
        response = self.client.post(reverse('solicitar_turno'), {'motivo': 'tramite'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Turno.objects.filter(usuario=self.estudiante, estado='espera').exists())

    def test_estado_cola_visible(self):
        self.client.login(username='ana@uta.edu.ec', password=self.user_password)
        response = self.client.get(reverse('estado_cola'))
        self.assertEqual(response.status_code, 200)

    def test_llamar_turno(self):
        turno = Turno.objects.create(codigo='T-001', usuario=self.estudiante, motivo='tramite', estado='espera')
        # Inyectar en la cola global (en una prueba real, el servidor se reinicia, 
        # pero aquí simulamos que la inicialización lo mete)
        from turnos.views import cola_espera
        cola_espera.encolar(turno.id)
        
        self.client.login(username='maria@uta.edu.ec', password=self.user_password)
        response = self.client.post(reverse('llamar_siguiente'))
        turno.refresh_from_db()
        self.assertEqual(turno.estado, 'llamado')

    def test_cola_fifo_orden(self):
        t1 = Turno.objects.create(codigo='T-001', usuario=self.estudiante, motivo='tramite', estado='espera')
        t2 = Turno.objects.create(codigo='T-002', usuario=self.estudiante, motivo='consulta', estado='espera')
        from turnos.views import cola_espera
        cola_espera.encolar(t1.id)
        cola_espera.encolar(t2.id)
        
        self.assertEqual(cola_espera.desencolar(), t1.id)
        self.assertEqual(cola_espera.desencolar(), t2.id)

class TramitesTests(TestCase):
    def setUp(self):
        self.user_password = 'Admin2026#'
        self.tipo = TipoTramite.objects.create(nombre="Certificado", activo=True)
        self.estudiante = Usuario.objects.create_user(
            username='luis', email='luis@uta.edu.ec', password=self.user_password, rol='estudiante'
        )
        self.otro_estudiante = Usuario.objects.create_user(
            username='ana', email='ana@uta.edu.ec', password=self.user_password, rol='estudiante'
        )
        self.admin = Usuario.objects.create_user(
            username='admin_tramites', email='admin_t@uta.edu.ec', password=self.user_password, rol='administrativo'
        )

    def test_crear_tramite(self):
        self.client.login(username='luis@uta.edu.ec', password=self.user_password)
        response = self.client.post(reverse('solicitar_tramite'), {
            'tipo': self.tipo.id,
            'descripcion': 'Prueba'
        })
        self.assertEqual(response.status_code, 302)
        tramite = Tramite.objects.get(solicitante=self.estudiante)
        self.assertEqual(tramite.estado, 'pendiente')
        self.assertIsNotNone(tramite.codigo)

    def test_listar_tramites_propios(self):
        Tramite.objects.create(codigo='TR-1', solicitante=self.estudiante, tipo=self.tipo, descripcion='P1')
        Tramite.objects.create(codigo='TR-2', solicitante=self.otro_estudiante, tipo=self.tipo, descripcion='P2')
        
        self.client.login(username='luis@uta.edu.ec', password=self.user_password)
        response = self.client.get(reverse('mis_tramites'))
        self.assertEqual(len(response.context['tramites']), 1)
        self.assertEqual(response.context['tramites'][0].codigo, 'TR-1')

    def test_cambiar_estado_tramite(self):
        tramite = Tramite.objects.create(codigo='TR-1', solicitante=self.estudiante, tipo=self.tipo, descripcion='P1')
        self.client.login(username='admin_t@uta.edu.ec', password=self.user_password)
        response = self.client.post(reverse('detalle_tramite_admin', args=[tramite.id]), {
            'estado_nuevo': 'en_proceso',
            'observacion': 'Atendiendo'
        })
        tramite.refresh_from_db()
        self.assertEqual(tramite.estado, 'en_proceso')
        self.assertTrue(HistorialEstadoTramite.objects.filter(tramite=tramite, estado_nuevo='en_proceso').exists())

    def test_estudiante_no_puede_cambiar_estado(self):
        tramite = Tramite.objects.create(codigo='TR-1', solicitante=self.estudiante, tipo=self.tipo, descripcion='P1')
        self.client.login(username='luis@uta.edu.ec', password=self.user_password)
        response = self.client.post(reverse('detalle_tramite_admin', args=[tramite.id]), {
            'estado_nuevo': 'en_proceso'
        })
        self.assertEqual(response.status_code, 302) # Redirige al dashboard por falta de permisos

class DocumentosTests(TestCase):
    def setUp(self):
        self.user_password = 'Admin2026#'
        self.admin = Usuario.objects.create_user(
            username='admin_docs', email='admin_d@uta.edu.ec', password=self.user_password, rol='admin'
        )
        self.estudiante = Usuario.objects.create_user(
            username='est', email='est@uta.edu.ec', password=self.user_password, rol='estudiante'
        )
        self.raiz = NodoJerarquico.objects.create(nombre="FISEI", tipo='facultad')

    def test_ver_jerarquia(self):
        self.client.login(username='est@uta.edu.ec', password=self.user_password)
        response = self.client.get(reverse('jerarquia'))
        self.assertEqual(response.status_code, 200)

    def test_crear_nodo_solo_admin(self):
        self.client.login(username='est@uta.edu.ec', password=self.user_password)
        response = self.client.post(reverse('crear_nodo'), {'nombre': 'Nuevo', 'tipo': 'area'})
        self.assertEqual(response.status_code, 302) # Redirige

    def test_crear_nodo_como_admin(self):
        self.client.login(username='admin_d@uta.edu.ec', password=self.user_password)
        response = self.client.post(reverse('crear_nodo'), {
            'nombre': 'Secretaria', 'tipo': 'departamento', 'padre': self.raiz.id
        })
        self.assertTrue(NodoJerarquico.objects.filter(nombre='Secretaria').exists())

    def test_buscar_documento(self):
        area = NodoJerarquico.objects.create(nombre="Area", tipo='area', padre=self.raiz)
        Documento.objects.create(nombre="Reglamento Interno", nodo=area)
        self.client.login(username='est@uta.edu.ec', password=self.user_password)
        response = self.client.get(reverse('jerarquia') + "?q=reglamento")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reglamento Interno")

class RutasTests(TestCase):
    def setUp(self):
        self.user_password = 'Admin2026#'
        self.estudiante = Usuario.objects.create_user(
            username='user_rutas', email='user_r@uta.edu.ec', password=self.user_password, rol='estudiante'
        )
        self.e1 = EspacioFisico.objects.create(nombre="A1", codigo="B1-A1", tipo="aula", bloque="1", piso=1)
        self.e2 = EspacioFisico.objects.create(nombre="A2", codigo="B1-A2", tipo="aula", bloque="1", piso=1)
        self.e3 = EspacioFisico.objects.create(nombre="A3", codigo="B1-A3", tipo="aula", bloque="1", piso=1)
        ConexionEspacio.objects.create(origen=self.e1, destino=self.e2, peso=10, bidireccional=True)

    def test_ver_mapa(self):
        self.client.login(username='user_r@uta.edu.ec', password=self.user_password)
        response = self.client.get(reverse('rutas:mapa'))
        self.assertEqual(response.status_code, 200)

    def test_buscar_ruta_valida(self):
        self.client.login(username='user_r@uta.edu.ec', password=self.user_password)
        response = self.client.post(reverse('rutas:buscar_ruta'), {
            'origen_id': self.e1.id,
            'destino_id': self.e2.id
        })
        self.assertIn(self.e1.id, response.context['ruta_ids'])
        self.assertIn(self.e2.id, response.context['ruta_ids'])

    def test_buscar_ruta_sin_conexion(self):
        self.client.login(username='user_r@uta.edu.ec', password=self.user_password)
        response = self.client.post(reverse('rutas:buscar_ruta'), {
            'origen_id': self.e1.id,
            'destino_id': self.e3.id
        })
        self.assertEqual(len(response.context['ruta_ids']), 0)

class HistorialTests(TestCase):
    def setUp(self):
        self.user_password = 'Admin2026#'
        self.estudiante = Usuario.objects.create_user(
            username='user_hist', email='user_h@uta.edu.ec', password=self.user_password, rol='estudiante'
        )
        self.admin = Usuario.objects.create_user(
            username='admin_hist', email='admin_h@uta.edu.ec', password=self.user_password, rol='admin'
        )

    def test_historial_registra_accion(self):
        registrar_accion(self.estudiante, 'rutas', 'Prueba', 'Detalle')
        self.assertTrue(HistorialAccion.objects.filter(usuario=self.estudiante, accion='Prueba').exists())

    def test_historial_visible(self):
        self.client.login(username='user_h@uta.edu.ec', password=self.user_password)
        response = self.client.get(reverse('historial:historial'))
        self.assertEqual(response.status_code, 200)

    def test_reporte_solo_admin(self):
        self.client.login(username='user_h@uta.edu.ec', password=self.user_password)
        response = self.client.get(reverse('historial:reportes'))
        self.assertEqual(response.status_code, 403)

    def test_reporte_con_filtros(self):
        self.client.login(username='admin_h@uta.edu.ec', password=self.user_password)
        response = self.client.post(reverse('historial:reportes'), {'estado': 'pendiente'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('tramites', response.context)

class EstructurasDatosTests(TestCase):
    def test_cola_fifo(self):
        cola = ColaFIFO()
        cola.encolar(1)
        cola.encolar(2)
        self.assertEqual(cola.desencolar(), 1)
        self.assertEqual(cola.desencolar(), 2)

    def test_cola_fifo_vacia(self):
        cola = ColaFIFO()
        self.assertIsNone(cola.desencolar())

    def test_pila_historial(self):
        pila = PilaHistorial(capacidad=3)
        pila.apilar(1)
        pila.apilar(2)
        self.assertEqual(pila.a_lista(), [2, 1])

    def test_pila_capacidad(self):
        pila = PilaHistorial(capacidad=2)
        pila.apilar(1)
        pila.apilar(2)
        pila.apilar(3)
        self.assertEqual(len(pila.a_lista()), 2)
        self.assertEqual(pila.a_lista()[0], 3)

    def test_lista_doble_navegacion(self):
        lista = HistorialListaDoble()
        lista.agregar_al_final(1)
        lista.agregar_al_final(2)
        lista.ir_inicio()
        self.assertEqual(lista.ir_siguiente(), 2)
        self.assertEqual(lista.ir_anterior(), 1)

    def test_lista_circular(self):
        lc = ListaCircular()
        lc.agregar("V1")
        lc.agregar("V2")
        self.assertEqual(lc.siguiente_ventanilla(), "V2")
        self.assertEqual(lc.siguiente_ventanilla(), "V1")
        self.assertEqual(lc.siguiente_ventanilla(), "V2")

    def test_arbol_nario_busqueda(self):
        raiz = NodoArbol({'id': 1, 'nombre': 'R'})
        h1 = NodoArbol({'id': 2, 'nombre': 'H1'})
        raiz.agregar_hijo(h1)
        arbol = ArbolNario(None)
        res = arbol.buscar_dfs(raiz, lambda x: x['id'] == 2)
        self.assertEqual(res.dato['nombre'], 'H1')

    def test_grafo_dijkstra(self):
        g = Grafo()
        g.agregar_arista(1, 2, 5)
        g.agregar_arista(2, 3, 5)
        g.agregar_arista(1, 3, 20)
        ruta, peso = g.dijkstra(1, 3)
        self.assertEqual(ruta, [1, 2, 3])
        self.assertEqual(peso, 10)

    def test_grafo_sin_ruta(self):
        g = Grafo()
        g.agregar_arista(1, 2, 5)
        ruta, peso = g.dijkstra(1, 3)
        self.assertEqual(len(ruta), 0)
