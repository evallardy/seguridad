from datetime import date

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from activos.models import AsignacionActivo
from asignaciones.models import AsignacionEmpleado
from .forms import (
    CertificacionForm,
    ContactoEmergenciaForm,
    DocumentoEmpleadoForm,
    EmpleadoCertificacionForm,
    EmpleadoForm,
    GroupForm,
    PuestoForm,
    TurnoForm,
    UserCreateForm,
    UserEmpleadoCreateForm,
    UserUpdateForm,
)
from .models import (
    Certificacion,
    ContactoEmergencia,
    DocumentoEmpleado,
    Empleado,
    EmpleadoCertificacion,
    Puesto,
    Turno,
)
from django.conf import settings


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "usuarios/dashboard.html"


class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = "usuarios/perfil.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        empleado = Empleado.objects.filter(user=user).first()
        context["empleado"] = empleado
        context["show_asignaciones"] = not user.groups.filter(
            name__in={"Admin", "Soporte"}
        ).exists()

        asignaciones_detalle = []
        if empleado and context["show_asignaciones"]:
            asignaciones = (
                AsignacionEmpleado.objects.filter(empleado=empleado, estatus="activo")
                .select_related(
                    "asignacion",
                    "asignacion__contrato",
                    "asignacion__sitio",
                    "asignacion__ruta",
                    "asignacion__equipo",
                )
                .order_by("-fecha_inicio")
            )
            activos = AsignacionActivo.objects.filter(asignacion__in=[a.asignacion for a in asignaciones])
            activos_por_asignacion = {}
            for activo in activos:
                activos_por_asignacion.setdefault(activo.asignacion_id, []).append(activo)

            for asignacion_empleado in asignaciones:
                asignacion = asignacion_empleado.asignacion
                fecha_fin = asignacion_empleado.fecha_fin or date.today()
                dias = None
                if asignacion_empleado.fecha_inicio:
                    dias = max((fecha_fin - asignacion_empleado.fecha_inicio).days, 0)
                asignaciones_detalle.append(
                    {
                        "asignacion": asignacion,
                        "asignacion_empleado": asignacion_empleado,
                        "activos": activos_por_asignacion.get(asignacion.id, []),
                        "dias": dias,
                    }
                )

        context["asignaciones_detalle"] = asignaciones_detalle
        return context


class AsignacionesHistoriaView(LoginRequiredMixin, TemplateView):
    template_name = "usuarios/asignaciones_historia.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.groups.filter(name__in={"Admin", "Soporte"}).exists():
            messages.error(self.request, "Tu perfil no tiene historial de asignaciones.")
            return redirect("usuarios:perfil")

        empleado = Empleado.objects.filter(user=user).first()
        context["empleado"] = empleado

        asignaciones_detalle = []
        if empleado:
            asignaciones = (
                AsignacionEmpleado.objects.filter(empleado=empleado)
                .select_related(
                    "asignacion",
                    "asignacion__contrato",
                    "asignacion__sitio",
                    "asignacion__ruta",
                    "asignacion__equipo",
                )
                .order_by("-fecha_inicio")
            )
            activos = AsignacionActivo.objects.filter(asignacion__in=[a.asignacion for a in asignaciones])
            activos_por_asignacion = {}
            for activo in activos:
                activos_por_asignacion.setdefault(activo.asignacion_id, []).append(activo)

            for asignacion_empleado in asignaciones:
                asignacion = asignacion_empleado.asignacion
                fecha_fin = asignacion_empleado.fecha_fin or date.today()
                dias = None
                if asignacion_empleado.fecha_inicio:
                    dias = max((fecha_fin - asignacion_empleado.fecha_inicio).days, 0)
                asignaciones_detalle.append(
                    {
                        "asignacion": asignacion,
                        "asignacion_empleado": asignacion_empleado,
                        "activos": activos_por_asignacion.get(asignacion.id, []),
                        "dias": dias,
                    }
                )

        context["asignaciones_detalle"] = asignaciones_detalle
        return context


class UsuariosPermissionMixin(PermissionRequiredMixin):
    raise_exception = True


class SearchableListView(ListView):
    paginate_by = 20
    search_fields = ()

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q", "").strip()
        if query and self.search_fields:
            filters = Q()
            for field in self.search_fields:
                filters |= Q(**{f"{field}__icontains": query})
            queryset = queryset.filter(filters)
        return queryset


class PuestoListView(LoginRequiredMixin, UsuariosPermissionMixin, SearchableListView):
    model = Puesto
    permission_required = "usuarios.view_puesto"
    template_name = "usuarios/puesto_list.html"
    search_fields = ("nombre",)


class PuestoCreateView(LoginRequiredMixin, UsuariosPermissionMixin, CreateView):
    model = Puesto
    permission_required = "usuarios.add_puesto"
    form_class = PuestoForm
    template_name = "usuarios/puesto_form.html"
    success_url = reverse_lazy("usuarios:puesto_list")


class PuestoUpdateView(LoginRequiredMixin, UsuariosPermissionMixin, UpdateView):
    model = Puesto
    permission_required = "usuarios.change_puesto"
    form_class = PuestoForm
    template_name = "usuarios/puesto_form.html"
    success_url = reverse_lazy("usuarios:puesto_list")


class PuestoDeleteView(LoginRequiredMixin, UsuariosPermissionMixin, DeleteView):
    model = Puesto
    permission_required = "usuarios.delete_puesto"
    template_name = "usuarios/puesto_confirm_delete.html"
    success_url = reverse_lazy("usuarios:puesto_list")


class TurnoListView(LoginRequiredMixin, UsuariosPermissionMixin, SearchableListView):
    model = Turno
    permission_required = "usuarios.view_turno"
    template_name = "usuarios/turno_list.html"
    search_fields = ("nombre", "dias_semana")


class TurnoCreateView(LoginRequiredMixin, UsuariosPermissionMixin, CreateView):
    model = Turno
    permission_required = "usuarios.add_turno"
    form_class = TurnoForm
    template_name = "usuarios/turno_form.html"
    success_url = reverse_lazy("usuarios:turno_list")


class TurnoUpdateView(LoginRequiredMixin, UsuariosPermissionMixin, UpdateView):
    model = Turno
    permission_required = "usuarios.change_turno"
    form_class = TurnoForm
    template_name = "usuarios/turno_form.html"
    success_url = reverse_lazy("usuarios:turno_list")


class TurnoDeleteView(LoginRequiredMixin, UsuariosPermissionMixin, DeleteView):
    model = Turno
    permission_required = "usuarios.delete_turno"
    template_name = "usuarios/turno_confirm_delete.html"
    success_url = reverse_lazy("usuarios:turno_list")


class EmpleadoListView(LoginRequiredMixin, UsuariosPermissionMixin, SearchableListView):
    model = Empleado
    permission_required = "usuarios.view_empleado"
    template_name = "usuarios/empleado_list.html"
    search_fields = ("nombres", "apellidos", "telefono", "email", "curp", "rfc")


class EmpleadoCreateView(LoginRequiredMixin, UsuariosPermissionMixin, CreateView):
    model = Empleado
    permission_required = "usuarios.add_empleado"
    form_class = EmpleadoForm
    template_name = "usuarios/empleado_form.html"
    success_url = reverse_lazy("usuarios:empleado_list")


class EmpleadoUpdateView(LoginRequiredMixin, UsuariosPermissionMixin, UpdateView):
    model = Empleado
    permission_required = "usuarios.change_empleado"
    form_class = EmpleadoForm
    template_name = "usuarios/empleado_form.html"
    success_url = reverse_lazy("usuarios:empleado_list")


class EmpleadoDeleteView(LoginRequiredMixin, UsuariosPermissionMixin, DeleteView):
    model = Empleado
    permission_required = "usuarios.delete_empleado"
    template_name = "usuarios/empleado_confirm_delete.html"
    success_url = reverse_lazy("usuarios:empleado_list")


class CertificacionListView(LoginRequiredMixin, UsuariosPermissionMixin, SearchableListView):
    model = Certificacion
    permission_required = "usuarios.view_certificacion"
    template_name = "usuarios/certificacion_list.html"
    search_fields = ("nombre", "organismo")


class CertificacionCreateView(LoginRequiredMixin, UsuariosPermissionMixin, CreateView):
    model = Certificacion
    permission_required = "usuarios.add_certificacion"
    form_class = CertificacionForm
    template_name = "usuarios/certificacion_form.html"
    success_url = reverse_lazy("usuarios:certificacion_list")


class CertificacionUpdateView(LoginRequiredMixin, UsuariosPermissionMixin, UpdateView):
    model = Certificacion
    permission_required = "usuarios.change_certificacion"
    form_class = CertificacionForm
    template_name = "usuarios/certificacion_form.html"
    success_url = reverse_lazy("usuarios:certificacion_list")


class CertificacionDeleteView(LoginRequiredMixin, UsuariosPermissionMixin, DeleteView):
    model = Certificacion
    permission_required = "usuarios.delete_certificacion"
    template_name = "usuarios/certificacion_confirm_delete.html"
    success_url = reverse_lazy("usuarios:certificacion_list")


class EmpleadoCertificacionListView(LoginRequiredMixin, UsuariosPermissionMixin, SearchableListView):
    model = EmpleadoCertificacion
    permission_required = "usuarios.view_empleadocertificacion"
    template_name = "usuarios/empleado_certificacion_list.html"
    search_fields = ("empleado__nombres", "empleado__apellidos", "certificacion__nombre")


class EmpleadoCertificacionCreateView(LoginRequiredMixin, UsuariosPermissionMixin, CreateView):
    model = EmpleadoCertificacion
    permission_required = "usuarios.add_empleadocertificacion"
    form_class = EmpleadoCertificacionForm
    template_name = "usuarios/empleado_certificacion_form.html"
    success_url = reverse_lazy("usuarios:empleado_certificacion_list")


class EmpleadoCertificacionUpdateView(LoginRequiredMixin, UsuariosPermissionMixin, UpdateView):
    model = EmpleadoCertificacion
    permission_required = "usuarios.change_empleadocertificacion"
    form_class = EmpleadoCertificacionForm
    template_name = "usuarios/empleado_certificacion_form.html"
    success_url = reverse_lazy("usuarios:empleado_certificacion_list")


class EmpleadoCertificacionDeleteView(LoginRequiredMixin, UsuariosPermissionMixin, DeleteView):
    model = EmpleadoCertificacion
    permission_required = "usuarios.delete_empleadocertificacion"
    template_name = "usuarios/empleado_certificacion_confirm_delete.html"
    success_url = reverse_lazy("usuarios:empleado_certificacion_list")


class DocumentoEmpleadoListView(LoginRequiredMixin, UsuariosPermissionMixin, SearchableListView):
    model = DocumentoEmpleado
    permission_required = "usuarios.view_documentoempleado"
    template_name = "usuarios/documento_empleado_list.html"
    search_fields = ("empleado__nombres", "empleado__apellidos", "tipo")


class DocumentoEmpleadoCreateView(LoginRequiredMixin, UsuariosPermissionMixin, CreateView):
    model = DocumentoEmpleado
    permission_required = "usuarios.add_documentoempleado"
    form_class = DocumentoEmpleadoForm
    template_name = "usuarios/documento_empleado_form.html"
    success_url = reverse_lazy("usuarios:documento_empleado_list")


class DocumentoEmpleadoUpdateView(LoginRequiredMixin, UsuariosPermissionMixin, UpdateView):
    model = DocumentoEmpleado
    permission_required = "usuarios.change_documentoempleado"
    form_class = DocumentoEmpleadoForm
    template_name = "usuarios/documento_empleado_form.html"
    success_url = reverse_lazy("usuarios:documento_empleado_list")


class DocumentoEmpleadoDeleteView(LoginRequiredMixin, UsuariosPermissionMixin, DeleteView):
    model = DocumentoEmpleado
    permission_required = "usuarios.delete_documentoempleado"
    template_name = "usuarios/documento_empleado_confirm_delete.html"
    success_url = reverse_lazy("usuarios:documento_empleado_list")


class ContactoEmergenciaListView(LoginRequiredMixin, UsuariosPermissionMixin, SearchableListView):
    model = ContactoEmergencia
    permission_required = "usuarios.view_contactoemergencia"
    template_name = "usuarios/contacto_emergencia_list.html"
    search_fields = ("empleado__nombres", "empleado__apellidos", "nombre", "telefono")


class ContactoEmergenciaCreateView(LoginRequiredMixin, UsuariosPermissionMixin, CreateView):
    model = ContactoEmergencia
    permission_required = "usuarios.add_contactoemergencia"
    form_class = ContactoEmergenciaForm
    template_name = "usuarios/contacto_emergencia_form.html"
    success_url = reverse_lazy("usuarios:contacto_emergencia_list")


class ContactoEmergenciaUpdateView(LoginRequiredMixin, UsuariosPermissionMixin, UpdateView):
    model = ContactoEmergencia
    permission_required = "usuarios.change_contactoemergencia"
    form_class = ContactoEmergenciaForm
    template_name = "usuarios/contacto_emergencia_form.html"
    success_url = reverse_lazy("usuarios:contacto_emergencia_list")


class ContactoEmergenciaDeleteView(LoginRequiredMixin, UsuariosPermissionMixin, DeleteView):
    model = ContactoEmergencia
    permission_required = "usuarios.delete_contactoemergencia"
    template_name = "usuarios/contacto_emergencia_confirm_delete.html"
    success_url = reverse_lazy("usuarios:contacto_emergencia_list")


User = get_user_model()


class UserListView(LoginRequiredMixin, UsuariosPermissionMixin, SearchableListView):
    model = User
    permission_required = "auth.view_user"
    template_name = "usuarios/user_list.html"
    search_fields = ("username", "email")


class UserCreateView(LoginRequiredMixin, UsuariosPermissionMixin, CreateView):
    model = User
    permission_required = "auth.add_user"
    form_class = UserCreateForm
    template_name = "usuarios/user_form.html"
    success_url = reverse_lazy("usuarios:user_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Usuario creado. Contrasena inicial: {settings.DEFAULT_INITIAL_PASSWORD}",
        )
        return response


class UserUpdateView(LoginRequiredMixin, UsuariosPermissionMixin, UpdateView):
    model = User
    permission_required = "auth.change_user"
    form_class = UserUpdateForm
    template_name = "usuarios/user_form.html"
    success_url = reverse_lazy("usuarios:user_list")


class UserDeleteView(LoginRequiredMixin, UsuariosPermissionMixin, DeleteView):
    model = User
    permission_required = "auth.delete_user"
    template_name = "usuarios/user_confirm_delete.html"
    success_url = reverse_lazy("usuarios:user_list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.groups.filter(name__in={"Admin", "Soporte"}).exists():
            messages.error(request, "No puedes eliminar usuarios Admin o Soporte.")
            return redirect(self.success_url)
        return super().delete(request, *args, **kwargs)


class UserEmpleadoCreateView(LoginRequiredMixin, UsuariosPermissionMixin, CreateView):
    model = User
    permission_required = ("auth.add_user", "usuarios.add_empleado")
    form_class = UserEmpleadoCreateForm
    template_name = "usuarios/user_empleado_form.html"
    success_url = reverse_lazy("usuarios:user_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        generated = getattr(form, "generated_username", None)
        if generated:
            messages.success(
                self.request,
                f"Usuario creado. Username asignado: {generated}. Contrasena inicial: {settings.DEFAULT_INITIAL_PASSWORD}",
            )
            return response
        messages.success(
            self.request,
            f"Usuario creado. Contrasena inicial: {settings.DEFAULT_INITIAL_PASSWORD}",
        )
        return response


class GroupListView(LoginRequiredMixin, UsuariosPermissionMixin, SearchableListView):
    model = Group
    permission_required = "auth.view_group"
    template_name = "usuarios/group_list.html"
    search_fields = ("name",)


class GroupCreateView(LoginRequiredMixin, UsuariosPermissionMixin, CreateView):
    model = Group
    permission_required = "auth.add_group"
    form_class = GroupForm
    template_name = "usuarios/group_form.html"
    success_url = reverse_lazy("usuarios:group_list")


class GroupUpdateView(LoginRequiredMixin, UsuariosPermissionMixin, UpdateView):
    model = Group
    permission_required = "auth.change_group"
    form_class = GroupForm
    template_name = "usuarios/group_form.html"
    success_url = reverse_lazy("usuarios:group_list")


class GroupDeleteView(LoginRequiredMixin, UsuariosPermissionMixin, DeleteView):
    model = Group
    permission_required = "auth.delete_group"
    template_name = "usuarios/group_confirm_delete.html"
    success_url = reverse_lazy("usuarios:group_list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.name in {"Admin", "Soporte"}:
            messages.error(request, "No puedes eliminar los grupos Admin o Soporte.")
            return redirect(self.success_url)
        return super().delete(request, *args, **kwargs)
