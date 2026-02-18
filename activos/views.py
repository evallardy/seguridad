from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from .forms import (
    ArmamentoForm,
    AsignacionActivoForm,
    RefaccionForm,
    RegistroCombustibleForm,
    VehiculoForm,
)
from .models import Armamento, AsignacionActivo, Refaccion, RegistroCombustible, Vehiculo


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "activos/home.html"


class ActivosPermissionMixin(PermissionRequiredMixin):
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
    number_field = None
    number_label = ""
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

        if self.number_field:
            num_from = self.request.GET.get("num_from")
            num_to = self.request.GET.get("num_to")
            if num_from:
                queryset = queryset.filter(**{f"{self.number_field}__gte": num_from})
            if num_to:
                queryset = queryset.filter(**{f"{self.number_field}__lte": num_to})

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
        context["show_number"] = bool(self.number_field)
        context["number_label"] = self.number_label
        context["order_choices"] = self.order_choices
        return context


class VehiculoListView(LoginRequiredMixin, ActivosPermissionMixin, SearchableListView):
    model = Vehiculo
    permission_required = "activos.view_vehiculo"
    template_name = "activos/vehiculo_list.html"
    search_fields = ("clave", "marca", "modelo", "placas", "serie", "tipo")
    status_field = "estatus"
    number_field = "km_actual"
    number_label = "KM"
    order_choices = (
        ("-fecha_alta", "Alta (reciente)"),
        ("fecha_alta", "Alta (antiguo)"),
        ("marca", "Marca (A-Z)"),
        ("-marca", "Marca (Z-A)"),
    )
    default_order = "-fecha_alta"


class VehiculoCreateView(LoginRequiredMixin, ActivosPermissionMixin, CreateView):
    model = Vehiculo
    permission_required = "activos.add_vehiculo"
    form_class = VehiculoForm
    template_name = "activos/vehiculo_form.html"
    success_url = reverse_lazy("activos:vehiculo_list")


class VehiculoUpdateView(LoginRequiredMixin, ActivosPermissionMixin, UpdateView):
    model = Vehiculo
    permission_required = "activos.change_vehiculo"
    form_class = VehiculoForm
    template_name = "activos/vehiculo_form.html"
    success_url = reverse_lazy("activos:vehiculo_list")


class VehiculoDeleteView(LoginRequiredMixin, ActivosPermissionMixin, DeleteView):
    model = Vehiculo
    permission_required = "activos.delete_vehiculo"
    template_name = "activos/vehiculo_confirm_delete.html"
    success_url = reverse_lazy("activos:vehiculo_list")


class ArmamentoListView(LoginRequiredMixin, ActivosPermissionMixin, SearchableListView):
    model = Armamento
    permission_required = "activos.view_armamento"
    template_name = "activos/armamento_list.html"
    search_fields = ("clave", "tipo", "marca", "modelo", "calibre", "numero_serie")
    status_field = "estatus"
    order_choices = (
        ("-fecha_alta", "Alta (reciente)"),
        ("fecha_alta", "Alta (antiguo)"),
        ("tipo", "Tipo (A-Z)"),
        ("-tipo", "Tipo (Z-A)"),
    )
    default_order = "-fecha_alta"


class ArmamentoCreateView(LoginRequiredMixin, ActivosPermissionMixin, CreateView):
    model = Armamento
    permission_required = "activos.add_armamento"
    form_class = ArmamentoForm
    template_name = "activos/armamento_form.html"
    success_url = reverse_lazy("activos:armamento_list")


class ArmamentoUpdateView(LoginRequiredMixin, ActivosPermissionMixin, UpdateView):
    model = Armamento
    permission_required = "activos.change_armamento"
    form_class = ArmamentoForm
    template_name = "activos/armamento_form.html"
    success_url = reverse_lazy("activos:armamento_list")


class ArmamentoDeleteView(LoginRequiredMixin, ActivosPermissionMixin, DeleteView):
    model = Armamento
    permission_required = "activos.delete_armamento"
    template_name = "activos/armamento_confirm_delete.html"
    success_url = reverse_lazy("activos:armamento_list")


class RefaccionListView(LoginRequiredMixin, ActivosPermissionMixin, SearchableListView):
    model = Refaccion
    permission_required = "activos.view_refaccion"
    template_name = "activos/refaccion_list.html"
    search_fields = ("nombre", "tipo_activo", "unidad")
    date_field = "fecha_alta"
    tipo_field = "tipo_activo"
    number_field = "costo_unitario"
    number_label = "Costo"
    order_choices = (
        ("-fecha_alta", "Alta (reciente)"),
        ("fecha_alta", "Alta (antiguo)"),
        ("nombre", "Nombre (A-Z)"),
        ("-nombre", "Nombre (Z-A)"),
        ("-costo_unitario", "Costo (alto)"),
        ("costo_unitario", "Costo (bajo)"),
    )
    default_order = "nombre"


class RefaccionCreateView(LoginRequiredMixin, ActivosPermissionMixin, CreateView):
    model = Refaccion
    permission_required = "activos.add_refaccion"
    form_class = RefaccionForm
    template_name = "activos/refaccion_form.html"
    success_url = reverse_lazy("activos:refaccion_list")


class RefaccionUpdateView(LoginRequiredMixin, ActivosPermissionMixin, UpdateView):
    model = Refaccion
    permission_required = "activos.change_refaccion"
    form_class = RefaccionForm
    template_name = "activos/refaccion_form.html"
    success_url = reverse_lazy("activos:refaccion_list")


class RefaccionDeleteView(LoginRequiredMixin, ActivosPermissionMixin, DeleteView):
    model = Refaccion
    permission_required = "activos.delete_refaccion"
    template_name = "activos/refaccion_confirm_delete.html"
    success_url = reverse_lazy("activos:refaccion_list")


class AsignacionActivoListView(LoginRequiredMixin, ActivosPermissionMixin, SearchableListView):
    model = AsignacionActivo
    permission_required = "activos.view_asignacionactivo"
    template_name = "activos/asignacion_activo_list.html"
    search_fields = ("asignacion__contrato__numero", "asignacion__sitio__nombre")

    def get_queryset(self):
        queryset = super().get_queryset()
        vehiculo_id = self.request.GET.get("vehiculo")
        if vehiculo_id:
            content_type = ContentType.objects.get_for_model(Vehiculo)
            queryset = queryset.filter(content_type=content_type, object_id=vehiculo_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehiculo_id = self.request.GET.get("vehiculo")
        context["vehiculo"] = (
            Vehiculo.objects.filter(pk=vehiculo_id).first() if vehiculo_id else None
        )
        return context


class AsignacionActivoCreateView(LoginRequiredMixin, ActivosPermissionMixin, CreateView):
    model = AsignacionActivo
    permission_required = "activos.add_asignacionactivo"
    form_class = AsignacionActivoForm
    template_name = "activos/asignacion_activo_form.html"
    success_url = reverse_lazy("activos:asignacion_activo_list")

    def get_initial(self):
        initial = super().get_initial()
        vehiculo_id = self.request.GET.get("vehiculo")
        if vehiculo_id:
            initial["content_type"] = ContentType.objects.get_for_model(Vehiculo)
            initial["object_id"] = vehiculo_id
        return initial


class AsignacionActivoUpdateView(LoginRequiredMixin, ActivosPermissionMixin, UpdateView):
    model = AsignacionActivo
    permission_required = "activos.change_asignacionactivo"
    form_class = AsignacionActivoForm
    template_name = "activos/asignacion_activo_form.html"
    success_url = reverse_lazy("activos:asignacion_activo_list")


class AsignacionActivoDeleteView(LoginRequiredMixin, ActivosPermissionMixin, DeleteView):
    model = AsignacionActivo
    permission_required = "activos.delete_asignacionactivo"
    template_name = "activos/asignacion_activo_confirm_delete.html"
    success_url = reverse_lazy("activos:asignacion_activo_list")


class RegistroCombustibleListView(LoginRequiredMixin, ActivosPermissionMixin, SearchableListView):
    model = RegistroCombustible
    permission_required = "activos.view_registrocombustible"
    template_name = "activos/registro_combustible_list.html"
    search_fields = ("vehiculo__clave", "proveedor")
    date_field = "fecha"

    def get_queryset(self):
        queryset = super().get_queryset()
        vehiculo_id = self.request.GET.get("vehiculo")
        if vehiculo_id:
            queryset = queryset.filter(vehiculo_id=vehiculo_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehiculo_id = self.request.GET.get("vehiculo")
        context["vehiculo"] = (
            Vehiculo.objects.filter(pk=vehiculo_id).first() if vehiculo_id else None
        )
        return context


class RegistroCombustibleCreateView(LoginRequiredMixin, ActivosPermissionMixin, CreateView):
    model = RegistroCombustible
    permission_required = "activos.add_registrocombustible"
    form_class = RegistroCombustibleForm
    template_name = "activos/registro_combustible_form.html"
    success_url = reverse_lazy("activos:registro_combustible_list")

    def get_initial(self):
        initial = super().get_initial()
        vehiculo_id = self.request.GET.get("vehiculo")
        if vehiculo_id:
            initial["vehiculo"] = vehiculo_id
        return initial


class RegistroCombustibleUpdateView(LoginRequiredMixin, ActivosPermissionMixin, UpdateView):
    model = RegistroCombustible
    permission_required = "activos.change_registrocombustible"
    form_class = RegistroCombustibleForm
    template_name = "activos/registro_combustible_form.html"
    success_url = reverse_lazy("activos:registro_combustible_list")


class RegistroCombustibleDeleteView(LoginRequiredMixin, ActivosPermissionMixin, DeleteView):
    model = RegistroCombustible
    permission_required = "activos.delete_registrocombustible"
    template_name = "activos/registro_combustible_confirm_delete.html"
    success_url = reverse_lazy("activos:registro_combustible_list")
