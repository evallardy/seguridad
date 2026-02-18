from django.contrib import admin

from .models import (
    Asignacion,
    AsignacionEmpleado,
    BitacoraAsignacion,
    Equipo,
    Ruta,
)

admin.site.register(Ruta)
admin.site.register(Equipo)
admin.site.register(Asignacion)
admin.site.register(AsignacionEmpleado)
admin.site.register(BitacoraAsignacion)
