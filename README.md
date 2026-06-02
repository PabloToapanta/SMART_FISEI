# SmartFISEI - Sistema de Gestión Académica Institucional (UTA)

SmartFISEI es una plataforma integral diseñada para la Facultad de Ingeniería en Sistemas, Electrónica e Industrial (FISEI) de la Universidad Técnica de Ambato. Este proyecto ha sido desarrollado para la materia de **Estructura de Datos**, integrando algoritmos clásicos y estructuras avanzadas en una aplicación web real utilizando Django.

## 🚀 Estructuras de Datos Implementadas
El sistema utiliza las siguientes estructuras para gestionar sus módulos:
- **Cola (FIFO)**: Gestión de turnos de atención.
- **Pila (LIFO)**: Historial de acciones recientes del usuario.
- **Lista Circular**: Distribución rotatoria de ventanillas de atención.
- **Lista Secuencial**: Catálogo de tipos de trámites institucionales.
- **Lista Doblemente Enlazada**: Seguimiento cronológico de estados de trámites y navegación de expedientes.
- **Árbol N-ario**: Organización jerárquica de dependencias y documentos de la facultad (Búsqueda DFS).
- **Grafos (Algoritmo de Dijkstra)**: Navegación interna y cálculo de rutas óptimas entre bloques y aulas de la FISEI.

---

## 🛠️ Instrucciones de Instalación en Windows

Sigue estos pasos para clonar y ejecutar el sistema en tu máquina local:

### 1. Requisitos Previos
Asegúrate de tener instalado:
- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

### 2. Clonar el Repositorio
Abre tu terminal (PowerShell o CMD) y ejecuta:
```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd PROYECTO_SMART
```

### 3. Crear y Activar Entorno Virtual
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 4. Instalar Dependencias
```bash
pip install django
```
*(Nota: El proyecto usa principalmente librerías estándar de Django y Vis.js vía CDN).*

### 5. Configurar la Base de Datos
Ejecuta las migraciones para crear las tablas necesarias:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Cargar Datos de Prueba
Para tener usuarios, trámites y el mapa de la facultad listos, ejecuta el script de configuración automática:
```bash
python setup_test_data.py
```
*(Este script creará el administrador, docentes, estudiantes y el mapa completo de la facultad).*

### 7. Iniciar el Servidor
```bash
python manage.py runserver
```

---

## 🔑 Credenciales de Acceso (Pruebas)
Puedes usar las siguientes cuentas creadas por el script `setup_test_data.py`:

| Rol | Correo Institucional | Contraseña |
|-----|----------------------|------------|
| **Administrador** | `admin@fisei.uta.edu.ec` | `Admin2026#` |
| **Administrativo** | `administrativo@fisei.uta.edu.ec` | `Admin2026#` |
| **Docente** | `docente@fisei.uta.edu.ec` | `Admin2026#` |
| **Estudiante** | `estudiante1@fisei.uta.edu.ec` | `Admin2026#` |

---

## 🧪 Pruebas del Sistema
Para verificar la integridad de las estructuras de datos y el funcionamiento de los módulos:
```bash
python manage.py test tests
```

---

## 📧 Contacto y Autores
Proyecto desarrollado para el Semestre 3 - Materia: Estructura de Datos.
**Facultad de Ingeniería en Sistemas, Electrónica e Industrial - UTA**
