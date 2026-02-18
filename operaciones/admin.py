from django.contrib import admin

from .models import Cliente, Contrato, Incidente, Requerimiento, Servicio, Sitio

admin.site.register(Cliente)
admin.site.register(Sitio)
admin.site.register(Servicio)
admin.site.register(Contrato)
admin.site.register(Requerimiento)
admin.site.register(Incidente)
