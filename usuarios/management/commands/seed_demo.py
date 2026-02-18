from datetime import date, datetime, time, timedelta
from decimal import Decimal

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils import timezone

from activos.models import Armamento, Refaccion, RegistroCombustible, Vehiculo
from asignaciones.models import Asignacion, AsignacionEmpleado, BitacoraAsignacion, Equipo, Ruta
from contabilidad.models import CentroCosto, Cuenta, Factura, Movimiento, RelacionCentroCosto
from mantenimiento.models import DetalleMantenimiento, Inspeccion, OrdenMantenimiento, ProgramacionMantenimiento
from operaciones.models import Cliente, Contrato, Incidente, Requerimiento, Servicio, Sitio
from tracking.models import Dispositivo, PermisoGPS, Ubicacion
from usuarios.models import Empleado, Puesto, Turno
from usuarios.management.commands.setup_roles import ROLE_PERMISSIONS


class Command(BaseCommand):
    help = "Crea datos demo: usuarios, empleados, activos y datos de prueba."

    def handle(self, *args, **options):
        self._ensure_groups()
        self._create_users()
        guardias = self._create_empleados_guardia()
        clientes, contratos, sitios = self._create_operaciones()
        rutas, asignaciones = self._create_asignaciones(guardias, contratos, sitios)
        vehiculos, armamentos = self._create_activos()
        self._create_mantenimiento(guardias, vehiculos, armamentos)
        self._create_tracking(guardias)
        self._create_contabilidad(clientes, contratos)
        self._create_bitacoras(asignaciones, guardias)
        self.stdout.write(self.style.SUCCESS("Datos demo generados."))

    def _ensure_groups(self):
        all_perms = list(Permission.objects.all())
        for role, apps in ROLE_PERMISSIONS.items():
            group, _ = Group.objects.get_or_create(name=role)
            if "*" in apps:
                perms = all_perms
            else:
                perms = [perm for perm in all_perms if perm.content_type.app_label in apps]
            group.permissions.set(perms)

    def _create_user(self, username, first, last, email, password, groups=None, is_staff=False, is_superuser=False):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "first_name": first,
                "last_name": last,
                "email": email,
                "is_staff": is_staff,
                "is_superuser": is_superuser,
            },
        )
        if created:
            user.set_password(password)
            user.save(update_fields=["password"])
        if groups:
            user.groups.set(groups)
        return user

    def _create_users(self):
        group_admin = Group.objects.get(name="Admin")
        group_soporte = Group.objects.get(name="Soporte")
        group_conta = Group.objects.get(name="Contabilidad")
        group_asig = Group.objects.get(name="Asignaciones")
        group_oper = Group.objects.get(name="Operaciones")
        group_act = Group.objects.get(name="Activos")
        group_mant = Group.objects.get(name="Mantenimiento")
        group_track = Group.objects.get(name="Tracking")
        group_users = Group.objects.get(name="Usuarios")

        self._create_user(
            "admin",
            "Admin",
            "General",
            "admin@example.com",
            "Admin1234!",
            groups=[group_admin],
            is_staff=True,
            is_superuser=True,
        )
        self._create_user(
            "soporte",
            "Soporte",
            "Tecnico",
            "soporte@example.com",
            "Soporte1234!",
            groups=[group_soporte],
            is_staff=True,
        )

        for idx in range(1, 4):
            self._create_user(
                f"contabilidad0{idx}",
                "Conta",
                f"User{idx}",
                f"conta{idx}@example.com",
                "Conta1234!",
                groups=[group_conta],
            )

        self._create_user(
            "asignaciones01",
            "Asignaciones",
            "User",
            "asignaciones01@example.com",
            "Asignaciones1234!",
            groups=[group_asig],
        )

        self._create_user(
            "operador01",
            "Operador",
            "Multimodulo",
            "operador01@example.com",
            "Operador1234!",
            groups=[group_oper, group_act, group_mant, group_track, group_users],
        )

    def _create_empleados_guardia(self):
        puesto, _ = Puesto.objects.get_or_create(
            nombre="Guardia de Seguridad",
            defaults={"descripcion": "Guardia operativo", "salario_base": Decimal("9000.00")},
        )
        turno_dia, _ = Turno.objects.get_or_create(
            nombre="Diurno",
            defaults={"hora_inicio": time(8, 0), "hora_fin": time(16, 0), "dias_semana": "Lun-Vie"},
        )
        turno_noche, _ = Turno.objects.get_or_create(
            nombre="Nocturno",
            defaults={"hora_inicio": time(16, 0), "hora_fin": time(0, 0), "dias_semana": "Lun-Vie"},
        )

        guardias = []
        for idx in range(1, 11):
            username = f"guardia{idx:02d}"
            user = self._create_user(
                username,
                "Guardia",
                f"{idx:02d}",
                f"guardia{idx:02d}@example.com",
                "Guardia1234!",
            )
            empleado, _ = Empleado.objects.get_or_create(
                user=user,
                defaults={
                    "nombres": f"Guardia {idx:02d}",
                    "apellidos": "Demo",
                    "telefono": f"555010{idx:02d}",
                    "email": user.email,
                    "fecha_ingreso": date.today() - timedelta(days=30 * idx),
                    "puesto": puesto,
                    "turno_preferido": turno_dia if idx % 2 else turno_noche,
                    "estatus": "activo",
                },
            )
            guardias.append(empleado)
        return guardias

    def _create_operaciones(self):
        clientes_data = [
            ("Cliente Alfa", "ALF010101AA1"),
            ("Cliente Beta", "BET010101BB2"),
            ("Cliente Gamma", "GAM010101CC3"),
        ]
        clientes = []
        for name, rfc in clientes_data:
            cliente, _ = Cliente.objects.get_or_create(
                nombre=name,
                defaults={
                    "rfc": rfc,
                    "contacto_principal": "Contacto Demo",
                    "telefono": "5551110000",
                    "email": "contacto@example.com",
                    "direccion": "Direccion demo",
                },
            )
            clientes.append(cliente)

        sitios = []
        for idx, cliente in enumerate(clientes, start=1):
            sitio, _ = Sitio.objects.get_or_create(
                cliente=cliente,
                nombre=f"Sitio {idx}",
                defaults={
                    "tipo": "Oficina",
                    "direccion": f"Calle {idx} No. {10 + idx}",
                    "ciudad": "Ciudad",
                    "estado": "Estado",
                    "latitud": Decimal("19.432600"),
                    "longitud": Decimal("-99.133200"),
                },
            )
            sitios.append(sitio)

        servicios_data = [
            ("Vigilancia", True, True, False),
            ("Custodia", True, False, False),
            ("Monitoreo", False, False, False),
        ]
        servicios = []
        for name, arm, veh, can in servicios_data:
            servicio, _ = Servicio.objects.get_or_create(
                nombre=name,
                defaults={
                    "descripcion": f"Servicio {name}",
                    "requiere_armamento": arm,
                    "requiere_vehiculo": veh,
                    "requiere_canino": can,
                },
            )
            servicios.append(servicio)

        contratos = []
        for idx, cliente in enumerate(clientes, start=1):
            contrato, _ = Contrato.objects.get_or_create(
                numero=f"C-{1000 + idx}",
                defaults={
                    "cliente": cliente,
                    "fecha_inicio": date.today() - timedelta(days=60),
                    "fecha_fin": date.today() + timedelta(days=365),
                    "estatus": "activo",
                    "condiciones": "Contrato demo",
                    "tarifa_base": Decimal("15000.00"),
                },
            )
            contratos.append(contrato)

        for idx, contrato in enumerate(contratos, start=1):
            Requerimiento.objects.get_or_create(
                contrato=contrato,
                servicio=servicios[idx % len(servicios)],
                sitio=sitios[idx % len(sitios)],
                defaults={
                    "cantidad_guardias": 2,
                    "cantidad_caninos": 0,
                    "vehiculos_requeridos": 1,
                    "armamento_requerido": 1,
                    "horario": "24/7",
                },
            )

        for idx, sitio in enumerate(sitios, start=1):
            Incidente.objects.get_or_create(
                sitio=sitio,
                fecha_hora=timezone.now() - timedelta(days=idx),
                tipo=f"Incidente {idx}",
                defaults={
                    "descripcion": "Incidente de prueba",
                    "severidad": "media",
                    "estatus": "activo",
                },
            )

        return clientes, contratos, sitios

    def _create_asignaciones(self, guardias, contratos, sitios):
        rutas = []
        for idx in range(1, 4):
            ruta, _ = Ruta.objects.get_or_create(
                nombre=f"Ruta {idx}",
                defaults={
                    "descripcion": "Ruta demo",
                    "origen": "Base",
                    "destino": "Sitio",
                    "distancia_km": Decimal("12.50"),
                },
            )
            rutas.append(ruta)

        equipo, _ = Equipo.objects.get_or_create(
            nombre="Equipo Alfa",
            defaults={"supervisor": guardias[0] if guardias else None},
        )

        asignaciones = []
        for idx, contrato in enumerate(contratos, start=1):
            asignacion, _ = Asignacion.objects.get_or_create(
                contrato=contrato,
                tipo="sitio" if idx % 2 else "ruta",
                defaults={
                    "sitio": sitios[idx % len(sitios)],
                    "ruta": rutas[idx % len(rutas)],
                    "fecha_inicio": date.today() - timedelta(days=10),
                    "estatus": "activo",
                    "equipo": equipo,
                },
            )
            asignaciones.append(asignacion)

        for idx, asignacion in enumerate(asignaciones, start=1):
            AsignacionEmpleado.objects.get_or_create(
                asignacion=asignacion,
                empleado=guardias[idx % len(guardias)],
                defaults={
                    "rol": "Guardia",
                    "fecha_inicio": date.today() - timedelta(days=10),
                    "estatus": "activo",
                },
            )

        return rutas, asignaciones

    def _create_activos(self):
        vehiculos = []
        for idx in range(1, 11):
            vehiculo, _ = Vehiculo.objects.get_or_create(
                clave=f"VH-{idx:03d}",
                defaults={
                    "marca": "Marca",
                    "modelo": f"Modelo {idx}",
                    "anio": 2020 + (idx % 5),
                    "placas": f"ABC{idx:03d}",
                    "serie": f"SERIE{idx:05d}",
                    "tipo": "Pickup",
                    "capacidad": "4",
                    "estatus": "activo",
                    "km_actual": 10000 + (idx * 250),
                    "fecha_alta": date.today() - timedelta(days=idx * 5),
                },
            )
            vehiculos.append(vehiculo)

        armamentos = []
        for idx in range(1, 11):
            armamento, _ = Armamento.objects.get_or_create(
                clave=f"AR-{idx:03d}",
                defaults={
                    "tipo": "Pistola",
                    "marca": "Marca",
                    "modelo": f"Modelo {idx}",
                    "calibre": "9mm",
                    "numero_serie": f"ARM{idx:05d}",
                    "estatus": "activo",
                    "fecha_alta": date.today() - timedelta(days=idx * 4),
                },
            )
            armamentos.append(armamento)

        refacciones = []
        for idx in range(1, 6):
            refaccion, _ = Refaccion.objects.get_or_create(
                nombre=f"Refaccion {idx}",
                defaults={
                    "tipo_activo": "vehiculo",
                    "unidad": "pieza",
                    "stock_minimo": 2,
                    "costo_unitario": Decimal("250.00"),
                    "fecha_alta": date.today() - timedelta(days=idx * 7),
                },
            )
            refacciones.append(refaccion)

        if vehiculos:
            RegistroCombustible.objects.get_or_create(
                vehiculo=vehiculos[0],
                fecha=timezone.now() - timedelta(days=1),
                litros=Decimal("45.50"),
                defaults={
                    "costo_total": Decimal("1200.00"),
                    "km": 12500,
                    "proveedor": "Gasolinera Demo",
                },
            )

        return vehiculos, armamentos

    def _create_mantenimiento(self, guardias, vehiculos, armamentos):
        if not vehiculos and not armamentos:
            return

        activo = vehiculos[0] if vehiculos else armamentos[0]
        content_type = ContentType.objects.get_for_model(activo)
        orden, _ = OrdenMantenimiento.objects.get_or_create(
            content_type=content_type,
            object_id=activo.id,
            defaults={
                "fecha_apertura": date.today() - timedelta(days=7),
                "estatus": "en_proceso",
                "motivo": "Servicio preventivo",
                "tecnico": guardias[0] if guardias else None,
                "costo_mano_obra": Decimal("500.00"),
            },
        )

        refaccion = Refaccion.objects.first()
        if refaccion:
            DetalleMantenimiento.objects.get_or_create(
                orden=orden,
                refaccion=refaccion,
                defaults={
                    "cantidad": 1,
                    "costo_unitario": refaccion.costo_unitario,
                },
            )

        ProgramacionMantenimiento.objects.get_or_create(
            content_type=content_type,
            object_id=activo.id,
            defaults={
                "frecuencia_km": 5000,
                "frecuencia_dias": 90,
                "proximo_servicio": date.today() + timedelta(days=45),
                "activo_registro": True,
            },
        )

        Inspeccion.objects.get_or_create(
            content_type=content_type,
            object_id=activo.id,
            fecha=date.today() - timedelta(days=2),
            defaults={
                "resultado": "OK",
                "observaciones": "Sin novedades",
                "realizado_por": guardias[0] if guardias else None,
            },
        )

    def _create_tracking(self, guardias):
        for idx, empleado in enumerate(guardias, start=1):
            dispositivo, _ = Dispositivo.objects.get_or_create(
                empleado=empleado,
                plataforma="android" if idx % 2 else "ios",
                defaults={
                    "alias": f"Dispositivo {idx}",
                    "estatus": "activo",
                    "ultimo_ping": timezone.now() - timedelta(minutes=idx * 5),
                },
            )
            PermisoGPS.objects.get_or_create(
                empleado=empleado,
                defaults={"otorgado": True, "revocado": False, "motivo": "Demo"},
            )
            Ubicacion.objects.get_or_create(
                empleado=empleado,
                dispositivo=dispositivo,
                latitud=Decimal("19.432600"),
                longitud=Decimal("-99.133200"),
                timestamp=timezone.now() - timedelta(minutes=idx),
                defaults={"bateria": 80, "precision": Decimal("5.50"), "origen": "app"},
            )

    def _create_contabilidad(self, clientes, contratos):
        cuentas_data = [
            ("Caja", "activo", "1001"),
            ("Ventas", "ingreso", "4001"),
            ("Nomina", "gasto", "5001"),
        ]
        cuentas = []
        for nombre, tipo, codigo in cuentas_data:
            cuenta, _ = Cuenta.objects.get_or_create(
                nombre=nombre,
                defaults={"tipo": tipo, "codigo": codigo, "activa": True},
            )
            cuentas.append(cuenta)

        centros = []
        for idx in range(1, 3):
            centro, _ = CentroCosto.objects.get_or_create(
                nombre=f"Centro {idx}",
                defaults={"descripcion": "Centro demo", "activo": True},
            )
            centros.append(centro)

        movimientos = []
        for idx, cuenta in enumerate(cuentas, start=1):
            movimiento, _ = Movimiento.objects.get_or_create(
                cuenta=cuenta,
                fecha=date.today() - timedelta(days=idx),
                tipo="ingreso" if cuenta.tipo == "ingreso" else "gasto",
                monto=Decimal("1000.00") + Decimal(idx * 100),
                defaults={
                    "descripcion": "Movimiento demo",
                    "referencia": f"REF-{idx:03d}",
                    "contrato": contratos[idx % len(contratos)] if contratos else None,
                },
            )
            movimientos.append(movimiento)

        for idx, movimiento in enumerate(movimientos, start=1):
            RelacionCentroCosto.objects.get_or_create(
                movimiento=movimiento,
                centro_costo=centros[idx % len(centros)],
            )

        for idx, cliente in enumerate(clientes, start=1):
            Factura.objects.get_or_create(
                cliente=cliente,
                folio=f"F-{2000 + idx}",
                fecha=date.today() - timedelta(days=idx * 3),
                defaults={
                    "subtotal": Decimal("8000.00"),
                    "impuestos": Decimal("1280.00"),
                    "total": Decimal("9280.00"),
                    "estatus": "pagada" if idx % 2 else "pendiente",
                    "contrato": contratos[idx % len(contratos)] if contratos else None,
                },
            )

    def _create_bitacoras(self, asignaciones, guardias):
        for idx, asignacion in enumerate(asignaciones, start=1):
            BitacoraAsignacion.objects.get_or_create(
                asignacion=asignacion,
                fecha_hora=timezone.now() - timedelta(hours=idx),
                evento=f"Ronda {idx}",
                defaults={
                    "descripcion": "Bitacora demo",
                    "reportado_por": guardias[idx % len(guardias)] if guardias else None,
                },
            )
