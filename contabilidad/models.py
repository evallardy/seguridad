from django.db import models


TIPO_CUENTA_CHOICES = [
    ("activo", "Activo"),
    ("pasivo", "Pasivo"),
    ("ingreso", "Ingreso"),
    ("gasto", "Gasto"),
    ("capital", "Capital"),
]

TIPO_MOV_CHOICES = [
    ("ingreso", "Ingreso"),
    ("gasto", "Gasto"),
]

ESTATUS_FACTURA_CHOICES = [
    ("pendiente", "Pendiente"),
    ("pagada", "Pagada"),
    ("cancelada", "Cancelada"),
]


class Cuenta(models.Model):
    nombre = models.CharField(max_length=120)
    tipo = models.CharField(max_length=20, choices=TIPO_CUENTA_CHOICES)
    codigo = models.CharField(max_length=40, blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class CentroCosto(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Movimiento(models.Model):
    cuenta = models.ForeignKey("Cuenta", on_delete=models.PROTECT)
    fecha = models.DateField()
    tipo = models.CharField(max_length=20, choices=TIPO_MOV_CHOICES)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    descripcion = models.TextField(blank=True)
    referencia = models.CharField(max_length=120, blank=True)
    contrato = models.ForeignKey(
        "operaciones.Contrato", null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.cuenta} - {self.monto}".strip()


class RelacionCentroCosto(models.Model):
    movimiento = models.ForeignKey("Movimiento", on_delete=models.CASCADE)
    centro_costo = models.ForeignKey("CentroCosto", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.movimiento} - {self.centro_costo}".strip()


class Factura(models.Model):
    cliente = models.ForeignKey("operaciones.Cliente", on_delete=models.PROTECT)
    contrato = models.ForeignKey(
        "operaciones.Contrato", null=True, blank=True, on_delete=models.SET_NULL
    )
    folio = models.CharField(max_length=40)
    fecha = models.DateField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    impuestos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estatus = models.CharField(
        max_length=20, choices=ESTATUS_FACTURA_CHOICES, default="pendiente"
    )

    def __str__(self):
        return f"{self.folio} - {self.cliente}".strip()
