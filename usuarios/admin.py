from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ['username', 'email', 'rol', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Información Institucional', {'fields': ('rol', 'cedula', 'telefono', 'activo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Institucional', {'fields': ('rol', 'cedula', 'telefono', 'activo')}),
    )

admin.site.register(Usuario, UsuarioAdmin)
