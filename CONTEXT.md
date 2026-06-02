## Contexto del proyecto SmartFISEI

- Django 4.x, Python 3.x, SQLite, Bootstrap 5 vía CDN
- Apps al mismo nivel que manage.py: usuarios, turnos, tramites, documentos, rutas, historial
- AUTH_USER_MODEL = 'usuarios.Usuario'
- Los modelos ya están en cada models.py
- Las estructuras de datos ya están en cada services.py
- Bootstrap 5 se carga solo desde CDN en base.html, sin npm ni webpack
- Login requerido en todas las vistas protegidas con @login_required o LoginRequiredMixin
- Roles: admin, administrativo, docente, estudiante — campo rol en Usuario
