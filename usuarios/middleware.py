from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            default_password = getattr(settings, "DEFAULT_INITIAL_PASSWORD", None)
            if default_password and request.user.check_password(default_password):
                allowed = {
                    reverse("password_change"),
                    reverse("password_change_done"),
                    reverse("logout"),
                }
                path = request.path
                if path not in allowed:
                    static_url = getattr(settings, "STATIC_URL", "") or ""
                    media_url = getattr(settings, "MEDIA_URL", "") or ""
                    if static_url and path.startswith(static_url):
                        return self.get_response(request)
                    if media_url and path.startswith(media_url):
                        return self.get_response(request)
                    messages.warning(
                        request,
                        "Debes cambiar tu contrasena temporal antes de continuar.",
                    )
                    return redirect("password_change")
        return self.get_response(request)
