from django.contrib import admin

from .models import Dispositivo, PermisoGPS, Ubicacion

admin.site.register(Dispositivo)
admin.site.register(PermisoGPS)
admin.site.register(Ubicacion)
