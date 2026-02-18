from django.db import models


ESTATUS_CHOICES = [
    ("activo", "Activo"),
    ("inactivo", "Inactivo"),
    ("cerrado", "Cerrado"),
]

SEVERIDAD_CHOICES = [
    ("baja", "Baja"),
    ("media", "Media"),
    ("alta", "Alta"),
]


class Cliente(models.Model):
    nombre = models.CharField(max_length=160)
    rfc = models.CharField(max_length=13, blank=True)
    contacto_principal = models.CharField(max_length=120, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default="activo")

    def __str__(self):
        return self.nombre


class Sitio(models.Model):
    cliente = models.ForeignKey("Cliente", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=160)
    tipo = models.CharField(max_length=80, blank=True)
    direccion = models.TextField()
    ciudad = models.CharField(max_length=80, blank=True)
    estado = models.CharField(max_length=80, blank=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default="activo")

    def __str__(self):
        return f"{self.cliente} - {self.nombre}".strip()


class Servicio(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    requiere_armamento = models.BooleanField(default=False)
    requiere_vehiculo = models.BooleanField(default=False)
    requiere_canino = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class Contrato(models.Model):
    cliente = models.ForeignKey("Cliente", on_delete=models.CASCADE)
    numero = models.CharField(max_length=40, unique=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default="activo")
    condiciones = models.TextField(blank=True)
    tarifa_base = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.cliente} - {self.numero}".strip()


class Requerimiento(models.Model):
    contrato = models.ForeignKey("Contrato", on_delete=models.CASCADE)
    servicio = models.ForeignKey("Servicio", on_delete=models.CASCADE)
    sitio = models.ForeignKey("Sitio", on_delete=models.CASCADE)
    cantidad_guardias = models.PositiveIntegerField(default=0)
    cantidad_caninos = models.PositiveIntegerField(default=0)
    vehiculos_requeridos = models.PositiveIntegerField(default=0)
    armamento_requerido = models.PositiveIntegerField(default=0)
    horario = models.CharField(max_length=120, blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.contrato} - {self.servicio}".strip()


class Incidente(models.Model):
    sitio = models.ForeignKey("Sitio", on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    tipo = models.CharField(max_length=80)
    descripcion = models.TextField()
    severidad = models.CharField(max_length=20, choices=SEVERIDAD_CHOICES, default="baja")
    reportado_por = models.ForeignKey(
        "usuarios.Empleado", null=True, blank=True, on_delete=models.SET_NULL
    )
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default="activo")
    evidencia = models.FileField(upload_to="operaciones/incidente_evidencias/", blank=True)

    def __str__(self):
        return f"{self.sitio} - {self.tipo}".strip()
