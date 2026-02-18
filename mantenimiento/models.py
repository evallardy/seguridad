from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


ESTATUS_CHOICES = [
    ("abierta", "Abierta"),
    ("en_proceso", "En proceso"),
    ("cerrada", "Cerrada"),
]


class OrdenMantenimiento(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=models.Q(app_label="activos", model__in=["vehiculo", "armamento"]),
    )
    object_id = models.PositiveIntegerField()
    activo = GenericForeignKey("content_type", "object_id")
    fecha_apertura = models.DateField()
    fecha_cierre = models.DateField(null=True, blank=True)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default="abierta")
    motivo = models.TextField(blank=True)
    tecnico = models.ForeignKey(
        "usuarios.Empleado", null=True, blank=True, on_delete=models.SET_NULL
    )
    costo_mano_obra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.activo} - {self.estatus}".strip()


class DetalleMantenimiento(models.Model):
    orden = models.ForeignKey("OrdenMantenimiento", on_delete=models.CASCADE)
    refaccion = models.ForeignKey("activos.Refaccion", on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.orden} - {self.refaccion}".strip()


class ProgramacionMantenimiento(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=models.Q(app_label="activos", model__in=["vehiculo", "armamento"]),
    )
    object_id = models.PositiveIntegerField()
    activo = GenericForeignKey("content_type", "object_id")
    frecuencia_km = models.PositiveIntegerField(default=0)
    frecuencia_dias = models.PositiveIntegerField(default=0)
    proximo_servicio = models.DateField(null=True, blank=True)
    activo_registro = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.activo} - {self.proximo_servicio}".strip()


class Inspeccion(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=models.Q(app_label="activos", model__in=["vehiculo", "armamento"]),
    )
    object_id = models.PositiveIntegerField()
    activo = GenericForeignKey("content_type", "object_id")
    fecha = models.DateField()
    resultado = models.CharField(max_length=80)
    observaciones = models.TextField(blank=True)
    realizado_por = models.ForeignKey(
        "usuarios.Empleado", null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.activo} - {self.resultado}".strip()
