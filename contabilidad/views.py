from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import models
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from .forms import (
    CentroCostoForm,
    CuentaForm,
    FacturaForm,
    MovimientoForm,
    RelacionCentroCostoForm,
)
from .models import CentroCosto, Cuenta, Factura, Movimiento, RelacionCentroCosto


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "contabilidad/home.html"


class ContabilidadPermissionMixin(PermissionRequiredMixin):
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
            field = self.model._meta.get_field(self.activo_field)
            if isinstance(field, models.BooleanField):
                if activo in ("1", "0", "true", "false", "True", "False"):
                    value = activo in ("1", "true", "True")
                    queryset = queryset.filter(**{self.activo_field: value})
            else:
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
        context["empleados"] = []
        context["show_tipo"] = bool(self.tipo_field)
        context["tipo_choices"] = (
            self.model._meta.get_field(self.tipo_field).choices if self.tipo_field else []
        )
        context["show_activo"] = bool(self.activo_field)
        if self.activo_field:
            field = self.model._meta.get_field(self.activo_field)
            if isinstance(field, models.BooleanField):
                context["activo_choices"] = (("1", "Si"), ("0", "No"))
            else:
                context["activo_choices"] = field.choices
        else:
            context["activo_choices"] = []
        context["show_plataforma"] = bool(self.plataforma_field)
        context["plataforma_choices"] = (
            self.model._meta.get_field(self.plataforma_field).choices if self.plataforma_field else []
        )
        context["order_choices"] = self.order_choices
        return context


class CuentaListView(LoginRequiredMixin, ContabilidadPermissionMixin, SearchableListView):
    model = Cuenta
    permission_required = "contabilidad.view_cuenta"
    template_name = "contabilidad/cuenta_list.html"
    search_fields = ("nombre", "codigo", "tipo")
    tipo_field = "tipo"
    order_choices = (
        ("nombre", "Nombre (A-Z)"),
        ("-nombre", "Nombre (Z-A)"),
        ("codigo", "Codigo (A-Z)"),
    )
    default_order = "nombre"


class CuentaCreateView(LoginRequiredMixin, ContabilidadPermissionMixin, CreateView):
    model = Cuenta
    permission_required = "contabilidad.add_cuenta"
    form_class = CuentaForm
    template_name = "contabilidad/cuenta_form.html"
    success_url = reverse_lazy("contabilidad:cuenta_list")


class CuentaUpdateView(LoginRequiredMixin, ContabilidadPermissionMixin, UpdateView):
    model = Cuenta
    permission_required = "contabilidad.change_cuenta"
    form_class = CuentaForm
    template_name = "contabilidad/cuenta_form.html"
    success_url = reverse_lazy("contabilidad:cuenta_list")


class CuentaDeleteView(LoginRequiredMixin, ContabilidadPermissionMixin, DeleteView):
    model = Cuenta
    permission_required = "contabilidad.delete_cuenta"
    template_name = "contabilidad/cuenta_confirm_delete.html"
    success_url = reverse_lazy("contabilidad:cuenta_list")


class CentroCostoListView(LoginRequiredMixin, ContabilidadPermissionMixin, SearchableListView):
    model = CentroCosto
    permission_required = "contabilidad.view_centrocosto"
    template_name = "contabilidad/centro_costo_list.html"
    search_fields = ("nombre", "descripcion")
    activo_field = "activo"
    order_choices = (
        ("nombre", "Nombre (A-Z)"),
        ("-nombre", "Nombre (Z-A)"),
    )
    default_order = "nombre"


class CentroCostoCreateView(LoginRequiredMixin, ContabilidadPermissionMixin, CreateView):
    model = CentroCosto
    permission_required = "contabilidad.add_centrocosto"
    form_class = CentroCostoForm
    template_name = "contabilidad/centro_costo_form.html"
    success_url = reverse_lazy("contabilidad:centro_costo_list")


class CentroCostoUpdateView(LoginRequiredMixin, ContabilidadPermissionMixin, UpdateView):
    model = CentroCosto
    permission_required = "contabilidad.change_centrocosto"
    form_class = CentroCostoForm
    template_name = "contabilidad/centro_costo_form.html"
    success_url = reverse_lazy("contabilidad:centro_costo_list")


class CentroCostoDeleteView(LoginRequiredMixin, ContabilidadPermissionMixin, DeleteView):
    model = CentroCosto
    permission_required = "contabilidad.delete_centrocosto"
    template_name = "contabilidad/centro_costo_confirm_delete.html"
    success_url = reverse_lazy("contabilidad:centro_costo_list")


class MovimientoListView(LoginRequiredMixin, ContabilidadPermissionMixin, SearchableListView):
    model = Movimiento
    permission_required = "contabilidad.view_movimiento"
    template_name = "contabilidad/movimiento_list.html"
    search_fields = ("descripcion", "referencia", "cuenta__nombre")
    date_field = "fecha"
    order_choices = (
        ("-fecha", "Fecha (reciente)"),
        ("fecha", "Fecha (antiguo)"),
        ("-monto", "Monto (alto)"),
        ("monto", "Monto (bajo)"),
    )
    default_order = "-fecha"


class MovimientoCreateView(LoginRequiredMixin, ContabilidadPermissionMixin, CreateView):
    model = Movimiento
    permission_required = "contabilidad.add_movimiento"
    form_class = MovimientoForm
    template_name = "contabilidad/movimiento_form.html"
    success_url = reverse_lazy("contabilidad:movimiento_list")


class MovimientoUpdateView(LoginRequiredMixin, ContabilidadPermissionMixin, UpdateView):
    model = Movimiento
    permission_required = "contabilidad.change_movimiento"
    form_class = MovimientoForm
    template_name = "contabilidad/movimiento_form.html"
    success_url = reverse_lazy("contabilidad:movimiento_list")


class MovimientoDeleteView(LoginRequiredMixin, ContabilidadPermissionMixin, DeleteView):
    model = Movimiento
    permission_required = "contabilidad.delete_movimiento"
    template_name = "contabilidad/movimiento_confirm_delete.html"
    success_url = reverse_lazy("contabilidad:movimiento_list")


class RelacionCentroCostoListView(
    LoginRequiredMixin, ContabilidadPermissionMixin, SearchableListView
):
    model = RelacionCentroCosto
    permission_required = "contabilidad.view_relacioncentrocosto"
    template_name = "contabilidad/relacion_centro_costo_list.html"
    search_fields = ("movimiento__descripcion", "centro_costo__nombre")
    order_choices = (
        ("-id", "Recientes"),
        ("id", "Antiguos"),
    )
    default_order = "-id"


class RelacionCentroCostoCreateView(LoginRequiredMixin, ContabilidadPermissionMixin, CreateView):
    model = RelacionCentroCosto
    permission_required = "contabilidad.add_relacioncentrocosto"
    form_class = RelacionCentroCostoForm
    template_name = "contabilidad/relacion_centro_costo_form.html"
    success_url = reverse_lazy("contabilidad:relacion_centro_costo_list")


class RelacionCentroCostoUpdateView(LoginRequiredMixin, ContabilidadPermissionMixin, UpdateView):
    model = RelacionCentroCosto
    permission_required = "contabilidad.change_relacioncentrocosto"
    form_class = RelacionCentroCostoForm
    template_name = "contabilidad/relacion_centro_costo_form.html"
    success_url = reverse_lazy("contabilidad:relacion_centro_costo_list")


class RelacionCentroCostoDeleteView(LoginRequiredMixin, ContabilidadPermissionMixin, DeleteView):
    model = RelacionCentroCosto
    permission_required = "contabilidad.delete_relacioncentrocosto"
    template_name = "contabilidad/relacion_centro_costo_confirm_delete.html"
    success_url = reverse_lazy("contabilidad:relacion_centro_costo_list")


class FacturaListView(LoginRequiredMixin, ContabilidadPermissionMixin, SearchableListView):
    model = Factura
    permission_required = "contabilidad.view_factura"
    template_name = "contabilidad/factura_list.html"
    search_fields = ("folio", "cliente__nombre")
    date_field = "fecha"
    status_field = "estatus"
    cliente_field = "cliente"
    order_choices = (
        ("-fecha", "Fecha (reciente)"),
        ("fecha", "Fecha (antiguo)"),
        ("-total", "Total (alto)"),
        ("total", "Total (bajo)"),
    )
    default_order = "-fecha"


class FacturaCreateView(LoginRequiredMixin, ContabilidadPermissionMixin, CreateView):
    model = Factura
    permission_required = "contabilidad.add_factura"
    form_class = FacturaForm
    template_name = "contabilidad/factura_form.html"
    success_url = reverse_lazy("contabilidad:factura_list")


class FacturaUpdateView(LoginRequiredMixin, ContabilidadPermissionMixin, UpdateView):
    model = Factura
    permission_required = "contabilidad.change_factura"
    form_class = FacturaForm
    template_name = "contabilidad/factura_form.html"
    success_url = reverse_lazy("contabilidad:factura_list")


class FacturaDeleteView(LoginRequiredMixin, ContabilidadPermissionMixin, DeleteView):
    model = Factura
    permission_required = "contabilidad.delete_factura"
    template_name = "contabilidad/factura_confirm_delete.html"
    success_url = reverse_lazy("contabilidad:factura_list")
