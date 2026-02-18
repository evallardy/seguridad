from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from .forms import (
    DetalleMantenimientoForm,
    InspeccionForm,
    OrdenMantenimientoForm,
    ProgramacionMantenimientoForm,
)
from .models import DetalleMantenimiento, Inspeccion, OrdenMantenimiento, ProgramacionMantenimiento
from activos.models import Vehiculo


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "mantenimiento/home.html"


class MantenimientoPermissionMixin(PermissionRequiredMixin):
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
        context["plataforma_choices"] = (
            self.model._meta.get_field(self.plataforma_field).choices if self.plataforma_field else []
        )
        context["order_choices"] = self.order_choices
        return context


class OrdenMantenimientoListView(LoginRequiredMixin, MantenimientoPermissionMixin, SearchableListView):
    model = OrdenMantenimiento
    permission_required = "mantenimiento.view_ordenmantenimiento"
    template_name = "mantenimiento/orden_list.html"
    search_fields = ("motivo", "tecnico__nombres", "tecnico__apellidos")
    status_field = "estatus"
    empleado_field = "tecnico"
    date_field = "fecha_apertura"
    order_choices = (
        ("-fecha_apertura", "Apertura (reciente)"),
        ("fecha_apertura", "Apertura (antiguo)"),
        ("estatus", "Estatus (A-Z)"),
    )
    default_order = "-fecha_apertura"

    def get_queryset(self):
        queryset = super().get_queryset()
        activo_type = self.request.GET.get("activo_type")
        activo_id = self.request.GET.get("activo_id")
        if activo_type == "vehiculo" and activo_id:
            content_type = ContentType.objects.get_for_model(Vehiculo)
            queryset = queryset.filter(content_type=content_type, object_id=activo_id)
        return queryset


class OrdenMantenimientoCreateView(LoginRequiredMixin, MantenimientoPermissionMixin, CreateView):
    model = OrdenMantenimiento
    permission_required = "mantenimiento.add_ordenmantenimiento"
    form_class = OrdenMantenimientoForm
    template_name = "mantenimiento/orden_form.html"
    success_url = reverse_lazy("mantenimiento:orden_list")


class OrdenMantenimientoUpdateView(LoginRequiredMixin, MantenimientoPermissionMixin, UpdateView):
    model = OrdenMantenimiento
    permission_required = "mantenimiento.change_ordenmantenimiento"
    form_class = OrdenMantenimientoForm
    template_name = "mantenimiento/orden_form.html"
    success_url = reverse_lazy("mantenimiento:orden_list")


class OrdenMantenimientoDeleteView(LoginRequiredMixin, MantenimientoPermissionMixin, DeleteView):
    model = OrdenMantenimiento
    permission_required = "mantenimiento.delete_ordenmantenimiento"
    template_name = "mantenimiento/orden_confirm_delete.html"
    success_url = reverse_lazy("mantenimiento:orden_list")


class DetalleMantenimientoListView(LoginRequiredMixin, MantenimientoPermissionMixin, SearchableListView):
    model = DetalleMantenimiento
    permission_required = "mantenimiento.view_detallemantenimiento"
    template_name = "mantenimiento/detalle_list.html"
    search_fields = ("refaccion__nombre",)
    order_choices = (
        ("-id", "Recientes"),
        ("id", "Antiguos"),
    )
    default_order = "-id"


class DetalleMantenimientoCreateView(LoginRequiredMixin, MantenimientoPermissionMixin, CreateView):
    model = DetalleMantenimiento
    permission_required = "mantenimiento.add_detallemantenimiento"
    form_class = DetalleMantenimientoForm
    template_name = "mantenimiento/detalle_form.html"
    success_url = reverse_lazy("mantenimiento:detalle_list")


class DetalleMantenimientoUpdateView(LoginRequiredMixin, MantenimientoPermissionMixin, UpdateView):
    model = DetalleMantenimiento
    permission_required = "mantenimiento.change_detallemantenimiento"
    form_class = DetalleMantenimientoForm
    template_name = "mantenimiento/detalle_form.html"
    success_url = reverse_lazy("mantenimiento:detalle_list")


class DetalleMantenimientoDeleteView(LoginRequiredMixin, MantenimientoPermissionMixin, DeleteView):
    model = DetalleMantenimiento
    permission_required = "mantenimiento.delete_detallemantenimiento"
    template_name = "mantenimiento/detalle_confirm_delete.html"
    success_url = reverse_lazy("mantenimiento:detalle_list")


class ProgramacionMantenimientoListView(
    LoginRequiredMixin, MantenimientoPermissionMixin, SearchableListView
):
    model = ProgramacionMantenimiento
    permission_required = "mantenimiento.view_programacionmantenimiento"
    template_name = "mantenimiento/programacion_list.html"
    search_fields = ("id",)
    order_choices = (
        ("-proximo_servicio", "Proximo (reciente)"),
        ("proximo_servicio", "Proximo (antiguo)"),
    )
    default_order = "-proximo_servicio"


class ProgramacionMantenimientoCreateView(
    LoginRequiredMixin, MantenimientoPermissionMixin, CreateView
):
    model = ProgramacionMantenimiento
    permission_required = "mantenimiento.add_programacionmantenimiento"
    form_class = ProgramacionMantenimientoForm
    template_name = "mantenimiento/programacion_form.html"
    success_url = reverse_lazy("mantenimiento:programacion_list")


class ProgramacionMantenimientoUpdateView(
    LoginRequiredMixin, MantenimientoPermissionMixin, UpdateView
):
    model = ProgramacionMantenimiento
    permission_required = "mantenimiento.change_programacionmantenimiento"
    form_class = ProgramacionMantenimientoForm
    template_name = "mantenimiento/programacion_form.html"
    success_url = reverse_lazy("mantenimiento:programacion_list")


class ProgramacionMantenimientoDeleteView(
    LoginRequiredMixin, MantenimientoPermissionMixin, DeleteView
):
    model = ProgramacionMantenimiento
    permission_required = "mantenimiento.delete_programacionmantenimiento"
    template_name = "mantenimiento/programacion_confirm_delete.html"
    success_url = reverse_lazy("mantenimiento:programacion_list")


class InspeccionListView(LoginRequiredMixin, MantenimientoPermissionMixin, SearchableListView):
    model = Inspeccion
    permission_required = "mantenimiento.view_inspeccion"
    template_name = "mantenimiento/inspeccion_list.html"
    search_fields = ("resultado", "realizado_por__nombres", "realizado_por__apellidos")
    empleado_field = "realizado_por"
    date_field = "fecha"
    order_choices = (
        ("-fecha", "Fecha (reciente)"),
        ("fecha", "Fecha (antiguo)"),
    )
    default_order = "-fecha"


class InspeccionCreateView(LoginRequiredMixin, MantenimientoPermissionMixin, CreateView):
    model = Inspeccion
    permission_required = "mantenimiento.add_inspeccion"
    form_class = InspeccionForm
    template_name = "mantenimiento/inspeccion_form.html"
    success_url = reverse_lazy("mantenimiento:inspeccion_list")


class InspeccionUpdateView(LoginRequiredMixin, MantenimientoPermissionMixin, UpdateView):
    model = Inspeccion
    permission_required = "mantenimiento.change_inspeccion"
    form_class = InspeccionForm
    template_name = "mantenimiento/inspeccion_form.html"
    success_url = reverse_lazy("mantenimiento:inspeccion_list")


class InspeccionDeleteView(LoginRequiredMixin, MantenimientoPermissionMixin, DeleteView):
    model = Inspeccion
    permission_required = "mantenimiento.delete_inspeccion"
    template_name = "mantenimiento/inspeccion_confirm_delete.html"
    success_url = reverse_lazy("mantenimiento:inspeccion_list")
