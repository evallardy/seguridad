from django.conf import settings
from django.db import models


ESTATUS_CHOICES = [
    ("activo", "Activo"),
    ("inactivo", "Inactivo"),
    ("baja", "Baja"),
]


class Puesto(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    salario_base = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    es_operativo = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Turno(models.Model):
    nombre = models.CharField(max_length=80)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    dias_semana = models.CharField(max_length=120)

    def __str__(self):
        return self.nombre


class Empleado(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120)
    curp = models.CharField(max_length=18, blank=True)
    rfc = models.CharField(max_length=13, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_ingreso = models.DateField(null=True, blank=True)
    puesto = models.ForeignKey("Puesto", null=True, blank=True, on_delete=models.SET_NULL)
    turno_preferido = models.ForeignKey(
        "Turno", null=True, blank=True, on_delete=models.SET_NULL
    )
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default="activo")
    foto = models.FileField(upload_to="usuarios/empleado_fotos/", blank=True)
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}".strip()


class Certificacion(models.Model):
    nombre = models.CharField(max_length=120)
    organismo = models.CharField(max_length=120, blank=True)
    vigencia_meses = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre


class EmpleadoCertificacion(models.Model):
    empleado = models.ForeignKey("Empleado", on_delete=models.CASCADE)
    certificacion = models.ForeignKey("Certificacion", on_delete=models.CASCADE)
    fecha_emision = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    documento = models.FileField(upload_to="usuarios/empleado_certificaciones/", blank=True)

    def __str__(self):
        return f"{self.empleado} - {self.certificacion}".strip()


class DocumentoEmpleado(models.Model):
    empleado = models.ForeignKey("Empleado", on_delete=models.CASCADE)
    tipo = models.CharField(max_length=80)
    archivo = models.FileField(upload_to="usuarios/empleado_documentos/")
    fecha_emision = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.empleado} - {self.tipo}".strip()


class ContactoEmergencia(models.Model):
    empleado = models.ForeignKey("Empleado", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=120)
    parentesco = models.CharField(max_length=60, blank=True)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.empleado} - {self.nombre}".strip()
