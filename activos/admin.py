from django.contrib import admin

from .models import (
    Armamento,
    AsignacionActivo,
    Combustible,
    InventarioMovimiento,
    Refaccion,
    RegistroCombustible,
    Vehiculo,
)

admin.site.register(Vehiculo)
admin.site.register(Armamento)
admin.site.register(Combustible)
admin.site.register(Refaccion)
admin.site.register(InventarioMovimiento)
admin.site.register(AsignacionActivo)
admin.site.register(RegistroCombustible)
