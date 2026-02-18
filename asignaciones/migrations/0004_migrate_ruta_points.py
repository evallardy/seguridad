from decimal import Decimal

from django.db import migrations


def forwards(apps, schema_editor):
    Ruta = apps.get_model("asignaciones", "Ruta")
    RutaPunto = apps.get_model("asignaciones", "RutaPunto")

    for ruta in Ruta.objects.all():
        if RutaPunto.objects.filter(ruta_id=ruta.id).exists():
            continue
        km_total = ruta.distancia_km or Decimal("0")
        RutaPunto.objects.create(
            ruta_id=ruta.id,
            orden=1,
            nombre=ruta.origen or "Origen",
            km_desde_anterior=Decimal("0"),
        )
        RutaPunto.objects.create(
            ruta_id=ruta.id,
            orden=2,
            nombre=ruta.destino or "Destino",
            km_desde_anterior=km_total,
        )


def backwards(apps, schema_editor):
    Ruta = apps.get_model("asignaciones", "Ruta")
    RutaPunto = apps.get_model("asignaciones", "RutaPunto")

    for ruta in Ruta.objects.all():
        puntos = list(RutaPunto.objects.filter(ruta_id=ruta.id).order_by("orden", "id"))
        if not puntos:
            continue
        ruta.origen = puntos[0].nombre
        ruta.destino = puntos[-1].nombre
        ruta.distancia_km = sum((p.km_desde_anterior or 0) for p in puntos)
        ruta.save(update_fields=["origen", "destino", "distancia_km"])


class Migration(migrations.Migration):
    dependencies = [
        ("asignaciones", "0003_rutapunto"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
