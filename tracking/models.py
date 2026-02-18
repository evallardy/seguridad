from django.db import models


ESTATUS_CHOICES = [
    ("activo", "Activo"),
    ("inactivo", "Inactivo"),
]

PLATAFORMA_CHOICES = [
    ("android", "Android"),
    ("ios", "iOS"),
    ("web", "Web"),
]

ORIGEN_CHOICES = [
    ("app", "App"),
    ("web", "Web"),
]


class Dispositivo(models.Model):
    empleado = models.ForeignKey("usuarios.Empleado", on_delete=models.CASCADE)
    alias = models.CharField(max_length=80, blank=True)
    plataforma = models.CharField(max_length=20, choices=PLATAFORMA_CHOICES)
    token_push = models.CharField(max_length=255, blank=True)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default="activo")
    ultimo_ping = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.empleado} - {self.plataforma}".strip()


class PermisoGPS(models.Model):
    empleado = models.ForeignKey("usuarios.Empleado", on_delete=models.CASCADE)
    otorgado = models.BooleanField(default=True)
    fecha_otorgado = models.DateTimeField(auto_now_add=True)
    revocado = models.BooleanField(default=False)
    fecha_revocado = models.DateTimeField(null=True, blank=True)
    motivo = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.empleado} - {self.otorgado}".strip()


class Ubicacion(models.Model):
    empleado = models.ForeignKey("usuarios.Empleado", on_delete=models.CASCADE)
    dispositivo = models.ForeignKey("Dispositivo", on_delete=models.CASCADE)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    bateria = models.PositiveSmallIntegerField(default=0)
    timestamp = models.DateTimeField()
    precision = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    origen = models.CharField(max_length=20, choices=ORIGEN_CHOICES, default="app")

    class Meta:
        indexes = [models.Index(fields=["timestamp"]) ]

    def __str__(self):
        return f"{self.empleado} - {self.timestamp}".strip()
