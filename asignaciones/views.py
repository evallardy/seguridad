from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from .forms import (
    AsignacionEmpleadoForm,
    AsignacionForm,
    EquipoForm,
    RutaForm,
    RutaPuntoForm,
)
from .models import Asignacion, AsignacionEmpleado, Equipo, Ruta, RutaPunto


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "asignaciones/home.html"


class AsignacionesPermissionMixin(PermissionRequiredMixin):
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
        context["clientes"] = (
            self.model._meta.apps.get_model("operaciones", "Cliente").objects.all()
            if self.cliente_field
            else []
        )
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


class RutaListView(LoginRequiredMixin, AsignacionesPermissionMixin, SearchableListView):
    model = Ruta
    permission_required = "asignaciones.view_ruta"
    template_name = "asignaciones/ruta_list.html"
    search_fields = ("nombre", "puntos__nombre")
    status_field = "estatus"
    order_choices = (
        ("nombre", "Nombre (A-Z)"),
        ("-nombre", "Nombre (Z-A)"),
        ("-id", "Recientes"),
    )
    default_order = "nombre"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("puntos")


class RutaCreateView(LoginRequiredMixin, AsignacionesPermissionMixin, CreateView):
    model = Ruta
    permission_required = "asignaciones.add_ruta"
    form_class = RutaForm
    template_name = "asignaciones/ruta_form.html"
    success_url = reverse_lazy("asignaciones:ruta_list")


class RutaUpdateView(LoginRequiredMixin, AsignacionesPermissionMixin, UpdateView):
    model = Ruta
    permission_required = "asignaciones.change_ruta"
    form_class = RutaForm
    template_name = "asignaciones/ruta_form.html"
    success_url = reverse_lazy("asignaciones:ruta_list")


class RutaDeleteView(LoginRequiredMixin, AsignacionesPermissionMixin, DeleteView):
    model = Ruta
    permission_required = "asignaciones.delete_ruta"
    template_name = "asignaciones/ruta_confirm_delete.html"
    success_url = reverse_lazy("asignaciones:ruta_list")


class RutaPuntoListView(LoginRequiredMixin, AsignacionesPermissionMixin, SearchableListView):
    model = RutaPunto
    permission_required = "asignaciones.view_rutapunto"
    template_name = "asignaciones/ruta_punto_list.html"
    search_fields = ("nombre",)

    def get_queryset(self):
        queryset = super().get_queryset().select_related("ruta")
        ruta_id = self.kwargs.get("ruta_id")
        if ruta_id:
            queryset = queryset.filter(ruta_id=ruta_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ruta_id = self.kwargs.get("ruta_id")
        context["ruta"] = Ruta.objects.filter(pk=ruta_id).first() if ruta_id else None
        return context


class RutaPuntoCreateView(LoginRequiredMixin, AsignacionesPermissionMixin, CreateView):
    model = RutaPunto
    permission_required = "asignaciones.add_rutapunto"
    form_class = RutaPuntoForm
    template_name = "asignaciones/ruta_punto_form.html"

    def form_valid(self, form):
        ruta_id = self.kwargs.get("ruta_id")
        if ruta_id:
            form.instance.ruta_id = ruta_id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("asignaciones:ruta_punto_list", kwargs={"ruta_id": self.kwargs.get("ruta_id")})


class RutaPuntoUpdateView(LoginRequiredMixin, AsignacionesPermissionMixin, UpdateView):
    model = RutaPunto
    permission_required = "asignaciones.change_rutapunto"
    form_class = RutaPuntoForm
    template_name = "asignaciones/ruta_punto_form.html"

    def get_success_url(self):
        return reverse_lazy("asignaciones:ruta_punto_list", kwargs={"ruta_id": self.object.ruta_id})


class RutaPuntoDeleteView(LoginRequiredMixin, AsignacionesPermissionMixin, DeleteView):
    model = RutaPunto
    permission_required = "asignaciones.delete_rutapunto"
    template_name = "asignaciones/ruta_punto_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("asignaciones:ruta_punto_list", kwargs={"ruta_id": self.object.ruta_id})


class EquipoListView(LoginRequiredMixin, AsignacionesPermissionMixin, SearchableListView):
    model = Equipo
    permission_required = "asignaciones.view_equipo"
    template_name = "asignaciones/equipo_list.html"
    search_fields = ("nombre", "supervisor__nombres", "supervisor__apellidos")
    status_field = "estatus"
    empleado_field = "supervisor"
    order_choices = (
        ("nombre", "Nombre (A-Z)"),
        ("-nombre", "Nombre (Z-A)"),
        ("-id", "Recientes"),
    )
    default_order = "nombre"


class EquipoCreateView(LoginRequiredMixin, AsignacionesPermissionMixin, CreateView):
    model = Equipo
    permission_required = "asignaciones.add_equipo"
    form_class = EquipoForm
    template_name = "asignaciones/equipo_form.html"
    success_url = reverse_lazy("asignaciones:equipo_list")


class EquipoUpdateView(LoginRequiredMixin, AsignacionesPermissionMixin, UpdateView):
    model = Equipo
    permission_required = "asignaciones.change_equipo"
    form_class = EquipoForm
    template_name = "asignaciones/equipo_form.html"
    success_url = reverse_lazy("asignaciones:equipo_list")


class EquipoDeleteView(LoginRequiredMixin, AsignacionesPermissionMixin, DeleteView):
    model = Equipo
    permission_required = "asignaciones.delete_equipo"
    template_name = "asignaciones/equipo_confirm_delete.html"
    success_url = reverse_lazy("asignaciones:equipo_list")


class AsignacionListView(LoginRequiredMixin, AsignacionesPermissionMixin, SearchableListView):
    model = Asignacion
    permission_required = "asignaciones.view_asignacion"
    template_name = "asignaciones/asignacion_list.html"
    search_fields = (
        "contrato__numero",
        "contrato__cliente__nombre",
        "sitio__nombre",
        "ruta__nombre",
        "tipo",
    )
    status_field = "estatus"
    tipo_field = "tipo"
    cliente_field = "contrato__cliente"
    date_field = "fecha_inicio"
    order_choices = (
        ("-fecha_inicio", "Inicio (reciente)"),
        ("fecha_inicio", "Inicio (antiguo)"),
        ("tipo", "Tipo (A-Z)"),
    )
    default_order = "-fecha_inicio"


class AsignacionCreateView(LoginRequiredMixin, AsignacionesPermissionMixin, CreateView):
    model = Asignacion
    permission_required = "asignaciones.add_asignacion"
    form_class = AsignacionForm
    template_name = "asignaciones/asignacion_form.html"
    success_url = reverse_lazy("asignaciones:asignacion_list")


class AsignacionUpdateView(LoginRequiredMixin, AsignacionesPermissionMixin, UpdateView):
    model = Asignacion
    permission_required = "asignaciones.change_asignacion"
    form_class = AsignacionForm
    template_name = "asignaciones/asignacion_form.html"
    success_url = reverse_lazy("asignaciones:asignacion_list")


class AsignacionDeleteView(LoginRequiredMixin, AsignacionesPermissionMixin, DeleteView):
    model = Asignacion
    permission_required = "asignaciones.delete_asignacion"
    template_name = "asignaciones/asignacion_confirm_delete.html"
    success_url = reverse_lazy("asignaciones:asignacion_list")


class AsignacionEmpleadoListView(LoginRequiredMixin, AsignacionesPermissionMixin, SearchableListView):
    model = AsignacionEmpleado
    permission_required = "asignaciones.view_asignacionempleado"
    template_name = "asignaciones/asignacion_empleado_list.html"
    search_fields = ("empleado__nombres", "empleado__apellidos", "rol")
    status_field = "estatus"
    empleado_field = "empleado"
    date_field = "fecha_inicio"
    order_choices = (
        ("-fecha_inicio", "Inicio (reciente)"),
        ("fecha_inicio", "Inicio (antiguo)"),
        ("-id", "Recientes"),
    )
    default_order = "-fecha_inicio"


class AsignacionEmpleadoCreateView(LoginRequiredMixin, AsignacionesPermissionMixin, CreateView):
    model = AsignacionEmpleado
    permission_required = "asignaciones.add_asignacionempleado"
    form_class = AsignacionEmpleadoForm
    template_name = "asignaciones/asignacion_empleado_form.html"
    success_url = reverse_lazy("asignaciones:asignacion_empleado_list")


class AsignacionEmpleadoUpdateView(LoginRequiredMixin, AsignacionesPermissionMixin, UpdateView):
    model = AsignacionEmpleado
    permission_required = "asignaciones.change_asignacionempleado"
    form_class = AsignacionEmpleadoForm
    template_name = "asignaciones/asignacion_empleado_form.html"
    success_url = reverse_lazy("asignaciones:asignacion_empleado_list")


class AsignacionEmpleadoDeleteView(LoginRequiredMixin, AsignacionesPermissionMixin, DeleteView):
    model = AsignacionEmpleado
    permission_required = "asignaciones.delete_asignacionempleado"
    template_name = "asignaciones/asignacion_empleado_confirm_delete.html"
    success_url = reverse_lazy("asignaciones:asignacion_empleado_list")
