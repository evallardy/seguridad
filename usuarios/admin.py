from django.contrib import admin

from .models import (
    Certificacion,
    ContactoEmergencia,
    DocumentoEmpleado,
    Empleado,
    EmpleadoCertificacion,
    Puesto,
    Turno,
)

admin.site.register(Puesto)
admin.site.register(Turno)
admin.site.register(Empleado)
admin.site.register(Certificacion)
admin.site.register(EmpleadoCertificacion)
admin.site.register(DocumentoEmpleado)
admin.site.register(ContactoEmergencia)
