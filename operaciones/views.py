from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from .forms import ClienteForm, ContratoForm, ServicioForm, SitioForm
from .models import Cliente, Contrato, Servicio, Sitio


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "operaciones/home.html"


class OperacionesPermissionMixin(PermissionRequiredMixin):
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
        context["clientes"] = Cliente.objects.all() if self.cliente_field else []
        context["show_empleado"] = bool(self.empleado_field)
        context["empleados"] = []
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


class ClienteListView(LoginRequiredMixin, OperacionesPermissionMixin, SearchableListView):
    model = Cliente
    permission_required = "operaciones.view_cliente"
    template_name = "operaciones/cliente_list.html"
    search_fields = ("nombre", "rfc", "contacto_principal", "telefono", "email")
    status_field = "estatus"
    order_choices = (
        ("nombre", "Nombre (A-Z)"),
        ("-nombre", "Nombre (Z-A)"),
        ("-id", "Recientes"),
    )
    default_order = "nombre"


class ClienteCreateView(LoginRequiredMixin, OperacionesPermissionMixin, CreateView):
    model = Cliente
    permission_required = "operaciones.add_cliente"
    form_class = ClienteForm
    template_name = "operaciones/cliente_form.html"
    success_url = reverse_lazy("operaciones:cliente_list")


class ClienteUpdateView(LoginRequiredMixin, OperacionesPermissionMixin, UpdateView):
    model = Cliente
    permission_required = "operaciones.change_cliente"
    form_class = ClienteForm
    template_name = "operaciones/cliente_form.html"
    success_url = reverse_lazy("operaciones:cliente_list")


class ClienteDeleteView(LoginRequiredMixin, OperacionesPermissionMixin, DeleteView):
    model = Cliente
    permission_required = "operaciones.delete_cliente"
    template_name = "operaciones/cliente_confirm_delete.html"
    success_url = reverse_lazy("operaciones:cliente_list")


class SitioListView(LoginRequiredMixin, OperacionesPermissionMixin, SearchableListView):
    model = Sitio
    permission_required = "operaciones.view_sitio"
    template_name = "operaciones/sitio_list.html"
    search_fields = ("nombre", "cliente__nombre", "ciudad", "estado", "direccion")
    status_field = "estatus"
    cliente_field = "cliente"
    order_choices = (
        ("nombre", "Nombre (A-Z)"),
        ("-nombre", "Nombre (Z-A)"),
        ("-id", "Recientes"),
    )
    default_order = "nombre"


class SitioCreateView(LoginRequiredMixin, OperacionesPermissionMixin, CreateView):
    model = Sitio
    permission_required = "operaciones.add_sitio"
    form_class = SitioForm
    template_name = "operaciones/sitio_form.html"
    success_url = reverse_lazy("operaciones:sitio_list")


class SitioUpdateView(LoginRequiredMixin, OperacionesPermissionMixin, UpdateView):
    model = Sitio
    permission_required = "operaciones.change_sitio"
    form_class = SitioForm
    template_name = "operaciones/sitio_form.html"
    success_url = reverse_lazy("operaciones:sitio_list")


class SitioDeleteView(LoginRequiredMixin, OperacionesPermissionMixin, DeleteView):
    model = Sitio
    permission_required = "operaciones.delete_sitio"
    template_name = "operaciones/sitio_confirm_delete.html"
    success_url = reverse_lazy("operaciones:sitio_list")


class ServicioListView(LoginRequiredMixin, OperacionesPermissionMixin, SearchableListView):
    model = Servicio
    permission_required = "operaciones.view_servicio"
    template_name = "operaciones/servicio_list.html"
    search_fields = ("nombre", "descripcion")
    order_choices = (
        ("nombre", "Nombre (A-Z)"),
        ("-nombre", "Nombre (Z-A)"),
        ("-id", "Recientes"),
    )
    default_order = "nombre"


class ServicioCreateView(LoginRequiredMixin, OperacionesPermissionMixin, CreateView):
    model = Servicio
    permission_required = "operaciones.add_servicio"
    form_class = ServicioForm
    template_name = "operaciones/servicio_form.html"
    success_url = reverse_lazy("operaciones:servicio_list")


class ServicioUpdateView(LoginRequiredMixin, OperacionesPermissionMixin, UpdateView):
    model = Servicio
    permission_required = "operaciones.change_servicio"
    form_class = ServicioForm
    template_name = "operaciones/servicio_form.html"
    success_url = reverse_lazy("operaciones:servicio_list")


class ServicioDeleteView(LoginRequiredMixin, OperacionesPermissionMixin, DeleteView):
    model = Servicio
    permission_required = "operaciones.delete_servicio"
    template_name = "operaciones/servicio_confirm_delete.html"
    success_url = reverse_lazy("operaciones:servicio_list")


class ContratoListView(LoginRequiredMixin, OperacionesPermissionMixin, SearchableListView):
    model = Contrato
    permission_required = "operaciones.view_contrato"
    template_name = "operaciones/contrato_list.html"
    search_fields = ("numero", "cliente__nombre", "condiciones")
    status_field = "estatus"
    cliente_field = "cliente"
    date_field = "fecha_inicio"
    order_choices = (
        ("-fecha_inicio", "Inicio (reciente)"),
        ("fecha_inicio", "Inicio (antiguo)"),
        ("numero", "Numero (A-Z)"),
    )
    default_order = "-fecha_inicio"


class ContratoCreateView(LoginRequiredMixin, OperacionesPermissionMixin, CreateView):
    model = Contrato
    permission_required = "operaciones.add_contrato"
    form_class = ContratoForm
    template_name = "operaciones/contrato_form.html"
    success_url = reverse_lazy("operaciones:contrato_list")


class ContratoUpdateView(LoginRequiredMixin, OperacionesPermissionMixin, UpdateView):
    model = Contrato
    permission_required = "operaciones.change_contrato"
    form_class = ContratoForm
    template_name = "operaciones/contrato_form.html"
    success_url = reverse_lazy("operaciones:contrato_list")


class ContratoDeleteView(LoginRequiredMixin, OperacionesPermissionMixin, DeleteView):
    model = Contrato
    permission_required = "operaciones.delete_contrato"
    template_name = "operaciones/contrato_confirm_delete.html"
    success_url = reverse_lazy("operaciones:contrato_list")
