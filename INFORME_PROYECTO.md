# INFORME TÉCNICO DE PROYECTO INTEGRADOR

**UNIVERSIDAD TÉCNICA DE AMBATO**  
**FACULTAD DE INGENIERÍA EN SISTEMAS, ELECTRÓNICA E INDUSTRIAL**  
**CARRERA DE INGENIERÍA DE SOFTWARE**

---

### 1. DATOS INFORMATIVOS
*   **Materia:** Estructura de Datos
*   **Docente:** Ing. Jose Caiza Mg.
*   **Semestre:** Tercero
*   **Paralelo:** "B"
*   **Integrantes:**
    *   Pablo Toapanta
    *   Estiven Chiluiza
    *   Jeampierre Ortiz
    *   David Rodriguez
*   **Proyecto:** SmartFISEI - Sistema de Gestión Institucional Basado en Estructuras de Datos

---

### 2. INTRODUCCIÓN
El presente proyecto, denominado **SmartFISEI**, consiste en el desarrollo de una plataforma web integral para la gestión de servicios académicos y administrativos de la Facultad de Ingeniería en Sistemas, Electrónica e Industrial. El objetivo principal es aplicar los conocimientos teóricos adquiridos en la asignatura de Estructura de Datos para resolver problemas de optimización, organización y flujo de información en un entorno institucional real.

---

### 3. DESCRIPCIÓN DE MÓDULOS Y ESTRUCTURAS DE DATOS

#### 3.1. Gestión de Usuarios y Autenticación
*   **Funcionalidad:** Permite el registro y validación de usuarios mediante correo institucional (`@uta.edu.ec`) y la asignación de roles (Estudiante, Docente, Administrativo, Admin).
*   **Seguridad:** Manejo de sesiones seguras y recuperación de contraseña mediante envío de correos simulados por consola.

#### 3.2. Módulo de Atención por Turnos
*   **Estructura:** **Cola (FIFO)** y **Lista Circular**.
*   **Aplicación:**
    *   **Cola (FIFO):** Los estudiantes solicitan turnos que se encolan por orden de llegada. El personal administrativo los extrae de la cola para asegurar una atención justa.
    *   **Lista Circular:** Se utiliza para la distribución rotatoria de turnos entre múltiples ventanillas activas, garantizando que la carga de trabajo sea equitativa para los administrativos.

#### 3.3. Módulo de Gestión de Trámites
*   **Estructura:** **Lista Secuencial** y **Lista Doblemente Enlazada**.
*   **Aplicación:**
    *   **Lista Secuencial:** Almacena el catálogo de los 15 tipos de trámites institucionales permitiendo un acceso indexado rápido para el usuario solicitante.
    *   **Lista Doblemente Enlazada:** Registra el historial de estados de cada trámite. Permite al administrativo y al estudiante navegar de forma bidireccional (atrás y adelante) entre los diferentes hitos del proceso (Pendiente -> En Proceso -> Resuelto).

#### 3.4. Módulo de Organización Documental Jerárquica
*   **Estructura:** **Árbol N-ario**.
*   **Aplicación:** Representa la jerarquía de la facultad (Departamentos -> Carreras -> Áreas). Permite asociar archivos PDF y documentos a cualquier nivel del árbol. La búsqueda de documentos se realiza mediante un recorrido de **Búsqueda en Profundidad (DFS)**.

#### 3.5. Módulo de Rutas Internas FISEI
*   **Estructura:** **Grafo (Algoritmo de Dijkstra)**.
*   **Aplicación:** Modela el mapa físico de la facultad (Bloques 1 y 2). Cada aula u oficina es un nodo y los pasillos son aristas con pesos (distancias en metros). El sistema calcula y visualiza la ruta más corta entre dos ubicaciones cualesquiera.

#### 3.6. Módulo de Historial y Reportes
*   **Estructura:** **Pila (LIFO)**.
*   **Aplicación:** Registra todas las acciones relevantes del usuario. Las acciones se "apilan", permitiendo que al consultar el historial, las actividades más recientes aparezcan siempre en la parte superior (el último en entrar es el primero en salir).

---

### 4. TECNOLOGÍAS UTILIZADAS
*   **Backend:** Python 3.x con Django Framework 4.x.
*   **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5.
*   **Visualización de Datos:** Vis.js Network para la representación de grafos e hilos jerárquicos.
*   **Base de Datos:** SQLite3 para persistencia de datos relacionales.
*   **Control de Versiones:** Git y GitHub.

---

### 5. CONCLUSIONES
*   La implementación de estructuras de datos personalizadas sobre un framework de alto nivel como Django demuestra que es posible optimizar procesos institucionales complejos.
*   El uso de Grafos y Árboles mejoró significativamente la experiencia de usuario al navegar por la facultad y consultar documentos jerarquizados.
*   Se logró integrar satisfactoriamente los requerimientos académicos con una interfaz moderna y funcional, cumpliendo con los estándares de la carrera de Ingeniería de Software.

---

**Ambato, Junio 2026**
