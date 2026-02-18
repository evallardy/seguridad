from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


ESTATUS_CHOICES = [
    ("activo", "Activo"),
    ("mantenimiento", "Mantenimiento"),
    ("baja", "Baja"),
]

TIPO_MOV_CHOICES = [
    ("entrada", "Entrada"),
    ("salida", "Salida"),
    ("ajuste", "Ajuste"),
]

TIPO_ACTIVO_CHOICES = [
    ("vehiculo", "Vehiculo"),
    ("armamento", "Armamento"),
]


class Vehiculo(models.Model):
    clave = models.CharField(max_length=40, unique=True)
    marca = models.CharField(max_length=80)
    modelo = models.CharField(max_length=80)
    anio = models.PositiveIntegerField()
    placas = models.CharField(max_length=20, blank=True)
    serie = models.CharField(max_length=40, blank=True)
    tipo = models.CharField(max_length=60, blank=True)
    capacidad = models.CharField(max_length=60, blank=True)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default="activo")
    km_actual = models.PositiveIntegerField(default=0)
    fecha_alta = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.clave} - {self.marca} {self.modelo}".strip()


class Armamento(models.Model):
    clave = models.CharField(max_length=40, unique=True)
    tipo = models.CharField(max_length=80)
    marca = models.CharField(max_length=80, blank=True)
    modelo = models.CharField(max_length=80, blank=True)
    calibre = models.CharField(max_length=40, blank=True)
    numero_serie = models.CharField(max_length=60, blank=True)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default="activo")
    fecha_alta = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.clave} - {self.tipo}".strip()


class Combustible(models.Model):
    tipo = models.CharField(max_length=40)
    unidad = models.CharField(max_length=20, default="litro")
    costo_promedio = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.tipo


class Refaccion(models.Model):
    nombre = models.CharField(max_length=120)
    tipo_activo = models.CharField(max_length=20, choices=TIPO_ACTIVO_CHOICES)
    unidad = models.CharField(max_length=20)
    stock_minimo = models.PositiveIntegerField(default=0)
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_alta = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class InventarioMovimiento(models.Model):
    tipo = models.CharField(max_length=20, choices=TIPO_MOV_CHOICES)
    refaccion = models.ForeignKey("Refaccion", on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha = models.DateTimeField()
    referencia = models.CharField(max_length=120, blank=True)
    realizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.refaccion} - {self.tipo}".strip()


class AsignacionActivo(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=models.Q(app_label="activos", model__in=["vehiculo", "armamento"]),
    )
    object_id = models.PositiveIntegerField()
    activo = GenericForeignKey("content_type", "object_id")
    asignacion = models.ForeignKey("asignaciones.Asignacion", on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default="activo")

    def __str__(self):
        return f"{self.asignacion} - {self.activo}".strip()


class RegistroCombustible(models.Model):
    vehiculo = models.ForeignKey("Vehiculo", on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    litros = models.DecimalField(max_digits=10, decimal_places=2)
    costo_total = models.DecimalField(max_digits=12, decimal_places=2)
    km = models.PositiveIntegerField(default=0)
    proveedor = models.CharField(max_length=120, blank=True)
    autorizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.vehiculo} - {self.fecha}".strip()
