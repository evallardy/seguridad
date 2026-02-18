from django.db import models


ESTATUS_CHOICES = [
    ("activo", "Activo"),
    ("inactivo", "Inactivo"),
    ("cerrado", "Cerrado"),
]

TIPO_ASIGNACION_CHOICES = [
    ("ruta", "Ruta"),
    ("sitio", "Sitio"),
]


class Ruta(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    origen = models.CharField(max_length=120)
    destino = models.CharField(max_length=120)
    distancia_km = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default="activo")

    def __str__(self):
        return self.nombre

    @property
    def total_km(self):
        total = self.puntos.aggregate(total=models.Sum("km_desde_anterior"))["total"]
        return total or 0

    @property
    def origen_nombre(self):
        primer = self.puntos.order_by("orden").first()
        return primer.nombre if primer else "-"

    @property
    def destino_nombre(self):
        ultimo = self.puntos.order_by("orden").last()
        return ultimo.nombre if ultimo else "-"

    @property
    def total_paradas(self):
        total = self.puntos.count()
        return max(total - 1, 0)


class RutaPunto(models.Model):
    ruta = models.ForeignKey("Ruta", on_delete=models.CASCADE, related_name="puntos")
    orden = models.PositiveIntegerField(default=1)
    nombre = models.CharField(max_length=120)
    km_desde_anterior = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ["orden", "id"]

    def __str__(self):
        return f"{self.ruta} - {self.orden}. {self.nombre}".strip()


class Equipo(models.Model):
    nombre = models.CharField(max_length=120)
    supervisor = models.ForeignKey(
        "usuarios.Empleado", null=True, blank=True, on_delete=models.SET_NULL
    )
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default="activo")

    def __str__(self):
        return self.nombre


class Asignacion(models.Model):
    tipo = models.CharField(max_length=20, choices=TIPO_ASIGNACION_CHOICES)
    contrato = models.ForeignKey("operaciones.Contrato", on_delete=models.CASCADE)
    sitio = models.ForeignKey(
        "operaciones.Sitio", null=True, blank=True, on_delete=models.SET_NULL
    )
    ruta = models.ForeignKey("Ruta", null=True, blank=True, on_delete=models.SET_NULL)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    turno = models.ForeignKey("usuarios.Turno", null=True, blank=True, on_delete=models.SET_NULL)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default="activo")
    observaciones = models.TextField(blank=True)
    equipo = models.ForeignKey("Equipo", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.contrato} - {self.tipo}".strip()


class AsignacionEmpleado(models.Model):
    asignacion = models.ForeignKey("Asignacion", on_delete=models.CASCADE)
    empleado = models.ForeignKey("usuarios.Empleado", on_delete=models.CASCADE)
    rol = models.CharField(max_length=80, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default="activo")

    def __str__(self):
        return f"{self.asignacion} - {self.empleado}".strip()


class BitacoraAsignacion(models.Model):
    asignacion = models.ForeignKey("Asignacion", on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    evento = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    reportado_por = models.ForeignKey(
        "usuarios.Empleado", null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.asignacion} - {self.evento}".strip()
