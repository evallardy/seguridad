from django.contrib import admin

from .models import DetalleMantenimiento, Inspeccion, OrdenMantenimiento, ProgramacionMantenimiento

admin.site.register(OrdenMantenimiento)
admin.site.register(DetalleMantenimiento)
admin.site.register(ProgramacionMantenimiento)
admin.site.register(Inspeccion)
