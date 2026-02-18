from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class DefaultPasswordValidator:
    def validate(self, password, user=None):
        default_password = getattr(settings, "DEFAULT_INITIAL_PASSWORD", None)
        if default_password and password == default_password:
            raise ValidationError(
                _("La contrasena temporal no se permite como contrasena final."),
                code="password_default",
            )

    def get_help_text(self):
        return _("No uses la contrasena temporal como contrasena final.")
