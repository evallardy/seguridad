from django.contrib import admin

from .models import CentroCosto, Cuenta, Factura, Movimiento, RelacionCentroCosto

admin.site.register(Cuenta)
admin.site.register(CentroCosto)
admin.site.register(Movimiento)
admin.site.register(RelacionCentroCosto)
admin.site.register(Factura)
