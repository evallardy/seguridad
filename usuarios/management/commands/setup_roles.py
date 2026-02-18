from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


ROLE_PERMISSIONS = {
    "Admin": ["*"],
    "Soporte": ["*"],
    "Operaciones": ["operaciones"],
    "Activos": ["activos"],
    "Asignaciones": ["asignaciones"],
    "Mantenimiento": ["mantenimiento"],
    "Tracking": ["tracking"],
    "Contabilidad": ["contabilidad"],
    "Usuarios": ["usuarios"],
}


class Command(BaseCommand):
    help = "Crea grupos base y asigna permisos por modulo."

    def handle(self, *args, **options):
        all_perms = list(Permission.objects.all())
        for role, apps in ROLE_PERMISSIONS.items():
            group, _ = Group.objects.get_or_create(name=role)
            if "*" in apps:
                perms = all_perms
            else:
                perms = [perm for perm in all_perms if perm.content_type.app_label in apps]
            group.permissions.set(perms)
            self.stdout.write(self.style.SUCCESS(f"Grupo '{role}' listo con {len(perms)} permisos."))
