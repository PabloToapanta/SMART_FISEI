# Guía de Pruebas - SmartFISEI

Este directorio contiene la suite de pruebas completa para verificar la funcionalidad del sistema y la correcta implementación de las estructuras de datos.

## Ejecución Completa
Para poblar la base de datos con datos de prueba y ejecutar todos los tests:
```bash
bash tests/run_tests.sh
```

## Ejecución por Grupos
Puedes ejecutar módulos específicos según tu necesidad:
- **Autenticación**: `python manage.py test tests.test_sistema_completo.AutenticacionTests`
- **Turnos (Cola/Circular)**: `python manage.py test tests.test_sistema_completo.TurnosTests`
- **Trámites (Lista Doble/Secuencial)**: `python manage.py test tests.test_sistema_completo.TramitesTests`
- **Documentos (Árbol N-ario)**: `python manage.py test tests.test_sistema_completo.DocumentosTests`
- **Rutas (Grafos)**: `python manage.py test tests.test_sistema_completo.RutasTests`
- **Historial (Pila)**: `python manage.py test tests.test_sistema_completo.HistorialTests`
- **Estructuras Unitarias**: `python manage.py test tests.test_sistema_completo.EstructurasDatosTests`

## Usuarios de Prueba (Contraseña: Admin2026#)
| Email | Rol | Uso |
|-------|-----|-----|
| admin@fisei.uta.edu.ec | admin | Reportes y gestión de nodos |
| administrativo@fisei.uta.edu.ec | administrativo | Atención de turnos y cambio de estados |
| docente@fisei.uta.edu.ec | docente | Solicitud de trámites y expedientes |
| estudiante1@fisei.uta.edu.ec | estudiante | Solicitud de turnos y trámites |

## Descripción de Grupos
1. **Autenticación**: Verifica login, logout y restricciones de acceso por rol.
2. **Turnos**: Valida el encolamiento FIFO y el llamado desde ventanillas.
3. **Trámites**: Prueba el registro de solicitudes y el seguimiento de estados.
4. **Documentos**: Verifica la navegación del árbol jerárquico y búsquedas DFS.
5. **Rutas**: Valida el algoritmo de Dijkstra para encontrar caminos óptimos.
6. **Historial**: Asegura que cada acción se registre correctamente en la pila.
7. **Estructuras**: Tests unitarios puros para cada clase en `services.py`.
