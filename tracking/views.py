from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from .forms import DispositivoForm, PermisoGPSForm, UbicacionForm
from .models import Dispositivo, PermisoGPS, Ubicacion


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tracking/home.html"


class TrackingPermissionMixin(PermissionRequiredMixin):
    raise_exception = True


class SearchableListView(ListView):
    paginate_by = 20
    search_fields = ()
    date_field = None
    status_field = None
    cliente_field = None
    empleado_field = None
    tipo_field = None
    activo_field = None
    plataforma_field = None
    order_choices = ()
    default_order = None

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q", "").strip()
        if query and self.search_fields:
            filters = Q()
            for field in self.search_fields:
                filters |= Q(**{f"{field}__icontains": query})
            queryset = queryset.filter(filters)

        if self.date_field:
            date_from = self.request.GET.get("date_from")
            date_to = self.request.GET.get("date_to")
            if date_from:
                queryset = queryset.filter(**{f"{self.date_field}__gte": date_from})
            if date_to:
                queryset = queryset.filter(**{f"{self.date_field}__lte": date_to})

        status = self.request.GET.get("status")
        if self.status_field and status:
            queryset = queryset.filter(**{self.status_field: status})

        cliente = self.request.GET.get("cliente")
        if self.cliente_field and cliente:
            queryset = queryset.filter(**{self.cliente_field: cliente})

        empleado = self.request.GET.get("empleado")
        if self.empleado_field and empleado:
            queryset = queryset.filter(**{self.empleado_field: empleado})

        tipo = self.request.GET.get("tipo")
        if self.tipo_field and tipo:
            queryset = queryset.filter(**{self.tipo_field: tipo})

        activo = self.request.GET.get("activo")
        if self.activo_field and activo:
            queryset = queryset.filter(**{self.activo_field: activo})

        plataforma = self.request.GET.get("plataforma")
        if self.plataforma_field and plataforma:
            queryset = queryset.filter(**{self.plataforma_field: plataforma})

        order = self.request.GET.get("order")
        valid_orders = {value for value, _ in self.order_choices}
        if order and order in valid_orders:
            queryset = queryset.order_by(order)
        elif self.default_order:
            queryset = queryset.order_by(self.default_order)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_date"] = bool(self.date_field)
        context["show_status"] = bool(self.status_field)
        context["status_choices"] = (
            self.model._meta.get_field(self.status_field).choices if self.status_field else []
        )
        context["show_cliente"] = bool(self.cliente_field)
        context["clientes"] = []
        context["show_empleado"] = bool(self.empleado_field)
        context["empleados"] = (
            self.model._meta.apps.get_model("usuarios", "Empleado").objects.all()
            if self.empleado_field
            else []
        )
        context["show_tipo"] = bool(self.tipo_field)
        context["tipo_choices"] = (
            self.model._meta.get_field(self.tipo_field).choices if self.tipo_field else []
        )
        context["show_activo"] = bool(self.activo_field)
        context["activo_choices"] = (
            self.model._meta.get_field(self.activo_field).choices if self.activo_field else []
        )
        context["show_plataforma"] = bool(self.plataforma_field)
        if self.plataforma_field:
            platform_model = self.model._meta.apps.get_model("tracking", "Dispositivo")
            context["plataforma_choices"] = platform_model._meta.get_field("plataforma").choices
        else:
            context["plataforma_choices"] = []
        context["order_choices"] = self.order_choices
        return context


class DispositivoListView(LoginRequiredMixin, TrackingPermissionMixin, SearchableListView):
    model = Dispositivo
    permission_required = "tracking.view_dispositivo"
    template_name = "tracking/dispositivo_list.html"
    search_fields = ("empleado__nombres", "empleado__apellidos", "alias", "plataforma")
    status_field = "estatus"
    plataforma_field = "plataforma"
    empleado_field = "empleado"
    order_choices = (
        ("-ultimo_ping", "Ultimo ping (reciente)"),
        ("ultimo_ping", "Ultimo ping (antiguo)"),
        ("alias", "Alias (A-Z)"),
    )
    default_order = "-ultimo_ping"


class DispositivoCreateView(LoginRequiredMixin, TrackingPermissionMixin, CreateView):
    model = Dispositivo
    permission_required = "tracking.add_dispositivo"
    form_class = DispositivoForm
    template_name = "tracking/dispositivo_form.html"
    success_url = reverse_lazy("tracking:dispositivo_list")


class DispositivoUpdateView(LoginRequiredMixin, TrackingPermissionMixin, UpdateView):
    model = Dispositivo
    permission_required = "tracking.change_dispositivo"
    form_class = DispositivoForm
    template_name = "tracking/dispositivo_form.html"
    success_url = reverse_lazy("tracking:dispositivo_list")


class DispositivoDeleteView(LoginRequiredMixin, TrackingPermissionMixin, DeleteView):
    model = Dispositivo
    permission_required = "tracking.delete_dispositivo"
    template_name = "tracking/dispositivo_confirm_delete.html"
    success_url = reverse_lazy("tracking:dispositivo_list")


class PermisoGPSListView(LoginRequiredMixin, TrackingPermissionMixin, SearchableListView):
    model = PermisoGPS
    permission_required = "tracking.view_permisogps"
    template_name = "tracking/permiso_list.html"
    search_fields = ("empleado__nombres", "empleado__apellidos", "motivo")
    empleado_field = "empleado"
    date_field = "fecha_otorgado"
    order_choices = (
        ("-fecha_otorgado", "Otorgado (reciente)"),
        ("fecha_otorgado", "Otorgado (antiguo)"),
    )
    default_order = "-fecha_otorgado"


class PermisoGPSCreateView(LoginRequiredMixin, TrackingPermissionMixin, CreateView):
    model = PermisoGPS
    permission_required = "tracking.add_permisogps"
    form_class = PermisoGPSForm
    template_name = "tracking/permiso_form.html"
    success_url = reverse_lazy("tracking:permiso_list")


class PermisoGPSUpdateView(LoginRequiredMixin, TrackingPermissionMixin, UpdateView):
    model = PermisoGPS
    permission_required = "tracking.change_permisogps"
    form_class = PermisoGPSForm
    template_name = "tracking/permiso_form.html"
    success_url = reverse_lazy("tracking:permiso_list")


class PermisoGPSDeleteView(LoginRequiredMixin, TrackingPermissionMixin, DeleteView):
    model = PermisoGPS
    permission_required = "tracking.delete_permisogps"
    template_name = "tracking/permiso_confirm_delete.html"
    success_url = reverse_lazy("tracking:permiso_list")


class UbicacionListView(LoginRequiredMixin, TrackingPermissionMixin, SearchableListView):
    model = Ubicacion
    permission_required = "tracking.view_ubicacion"
    template_name = "tracking/ubicacion_list.html"
    search_fields = ("empleado__nombres", "empleado__apellidos", "dispositivo__alias")
    empleado_field = "empleado"
    plataforma_field = "dispositivo__plataforma"
    date_field = "timestamp__date"
    order_choices = (
        ("-timestamp", "Timestamp (reciente)"),
        ("timestamp", "Timestamp (antiguo)"),
    )
    default_order = "-timestamp"


class UbicacionCreateView(LoginRequiredMixin, TrackingPermissionMixin, CreateView):
    model = Ubicacion
    permission_required = "tracking.add_ubicacion"
    form_class = UbicacionForm
    template_name = "tracking/ubicacion_form.html"
    success_url = reverse_lazy("tracking:ubicacion_list")


class UbicacionUpdateView(LoginRequiredMixin, TrackingPermissionMixin, UpdateView):
    model = Ubicacion
    permission_required = "tracking.change_ubicacion"
    form_class = UbicacionForm
    template_name = "tracking/ubicacion_form.html"
    success_url = reverse_lazy("tracking:ubicacion_list")


class UbicacionDeleteView(LoginRequiredMixin, TrackingPermissionMixin, DeleteView):
    model = Ubicacion
    permission_required = "tracking.delete_ubicacion"
    template_name = "tracking/ubicacion_confirm_delete.html"
    success_url = reverse_lazy("tracking:ubicacion_list")
