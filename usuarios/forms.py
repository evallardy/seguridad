import unicodedata

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.db import transaction

from .models import (
    Certificacion,
    ContactoEmergencia,
    DocumentoEmpleado,
    Empleado,
    EmpleadoCertificacion,
    ESTATUS_CHOICES,
    Puesto,
    Turno,
)


PROTECTED_GROUPS = {"Admin", "Soporte"}


class BaseBootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                continue
            css_class = field.widget.attrs.get("class", "")
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs["class"] = (css_class + " form-select").strip()
            else:
                field.widget.attrs["class"] = (css_class + " form-control").strip()


class PuestoForm(BaseBootstrapForm):
    class Meta:
        model = Puesto
        fields = "__all__"


class TurnoForm(BaseBootstrapForm):
    class Meta:
        model = Turno
        fields = "__all__"


class EmpleadoForm(BaseBootstrapForm):
    class Meta:
        model = Empleado
        exclude = ("user",)
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
            "fecha_ingreso": forms.DateInput(attrs={"type": "date"}),
        }


class CertificacionForm(BaseBootstrapForm):
    class Meta:
        model = Certificacion
        fields = "__all__"


class EmpleadoCertificacionForm(BaseBootstrapForm):
    class Meta:
        model = EmpleadoCertificacion
        fields = "__all__"

    def clean(self):
        cleaned = super().clean()
        fecha_emision = cleaned.get("fecha_emision")
        fecha_vencimiento = cleaned.get("fecha_vencimiento")
        if fecha_emision and fecha_vencimiento and fecha_vencimiento < fecha_emision:
            self.add_error(
                "fecha_vencimiento", "La fecha vencimiento no puede ser menor a la fecha emision."
            )
        return cleaned


class DocumentoEmpleadoForm(BaseBootstrapForm):
    class Meta:
        model = DocumentoEmpleado
        fields = "__all__"

    def clean(self):
        cleaned = super().clean()
        fecha_emision = cleaned.get("fecha_emision")
        fecha_vencimiento = cleaned.get("fecha_vencimiento")
        if fecha_emision and fecha_vencimiento and fecha_vencimiento < fecha_emision:
            self.add_error(
                "fecha_vencimiento", "La fecha vencimiento no puede ser menor a la fecha emision."
            )
        return cleaned


class ContactoEmergenciaForm(BaseBootstrapForm):
    class Meta:
        model = ContactoEmergencia
        fields = "__all__"


User = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "is_active", "groups", "user_permissions")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("password1", None)
        self.fields.pop("password2", None)
        self.fields["user_permissions"].queryset = Permission.objects.select_related(
            "content_type"
        )
        for field in self.fields.values():
            if isinstance(field.widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                continue
            css_class = field.widget.attrs.get("class", "")
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs["class"] = (css_class + " form-select").strip()
            else:
                field.widget.attrs["class"] = (css_class + " form-control").strip()

    def save(self, commit=True):
        user = forms.ModelForm.save(self, commit=False)
        user.set_password(settings.DEFAULT_INITIAL_PASSWORD)
        if commit:
            user.save()
            self.save_m2m()
        return user


class UserUpdateForm(BaseBootstrapForm):
    class Meta:
        model = User
        fields = ("username", "email", "is_active", "groups", "user_permissions")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_permissions"].queryset = Permission.objects.select_related(
            "content_type"
        )

    def clean_is_active(self):
        is_active = self.cleaned_data.get("is_active")
        if not is_active and self.instance.groups.filter(name__in=PROTECTED_GROUPS).exists():
            raise forms.ValidationError("No puedes desactivar usuarios Admin o Soporte.")
        return is_active


class GroupForm(BaseBootstrapForm):
    class Meta:
        model = Group
        fields = ("name", "permissions")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["permissions"].queryset = self.fields["permissions"].queryset.select_related(
            "content_type"
        )

    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        if self.instance.pk and self.instance.name in PROTECTED_GROUPS and name != self.instance.name:
            raise forms.ValidationError("No puedes renombrar los grupos Admin o Soporte.")
        return name


class UserEmpleadoCreateForm(UserCreationForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    is_active = forms.BooleanField(required=False, initial=True)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), required=False, widget=forms.SelectMultiple
    )
    nombres = forms.CharField(max_length=120)
    apellidos = forms.CharField(max_length=120)
    curp = forms.CharField(max_length=18, required=False)
    rfc = forms.CharField(max_length=13, required=False)
    telefono = forms.CharField(max_length=20, required=False)
    email_empleado = forms.EmailField(required=False)
    direccion = forms.CharField(widget=forms.Textarea, required=False)
    fecha_nacimiento = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    fecha_ingreso = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    puesto = forms.ModelChoiceField(queryset=Puesto.objects.all(), required=False)
    turno_preferido = forms.ModelChoiceField(queryset=Turno.objects.all(), required=False)
    estatus = forms.ChoiceField(choices=ESTATUS_CHOICES, initial="activo")
    foto = forms.FileField(required=False)
    notas = forms.CharField(widget=forms.Textarea, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "is_active", "groups")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("password1", None)
        self.fields.pop("password2", None)
        self.fields["username"].widget.attrs["readonly"] = True
        self.fields["username"].widget.attrs["placeholder"] = "Se genera automaticamente"
        for field in self.fields.values():
            if isinstance(field.widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                continue
            css_class = field.widget.attrs.get("class", "")
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs["class"] = (css_class + " form-select").strip()
            else:
                field.widget.attrs["class"] = (css_class + " form-control").strip()

    def clean(self):
        cleaned = super().clean()
        fecha_nacimiento = cleaned.get("fecha_nacimiento")
        fecha_ingreso = cleaned.get("fecha_ingreso")
        if fecha_nacimiento and fecha_ingreso and fecha_ingreso < fecha_nacimiento:
            self.add_error(
                "fecha_ingreso",
                "La fecha de ingreso no puede ser menor a la fecha de nacimiento.",
            )
        nombres = cleaned.get("nombres", "")
        apellidos = cleaned.get("apellidos", "")
        if nombres and apellidos:
            self.generated_username = self._build_username(nombres, apellidos)
            cleaned["username"] = self.generated_username
        return cleaned

    def _build_username(self, nombres, apellidos):
        nombre_base = (nombres.split() or [""])[0][:1]
        apellidos_parts = apellidos.split()
        paterno = apellidos_parts[0] if apellidos_parts else ""
        materno = apellidos_parts[1] if len(apellidos_parts) > 1 else "a"
        base = f"{nombre_base}.{paterno}.{materno}".strip(".")
        base = unicodedata.normalize("NFKD", base).encode("ascii", "ignore").decode("ascii")
        base = base.replace(" ", "").lower()
        username = base
        counter = 1
        while User.objects.filter(username=username).exists():
            counter += 1
            username = f"{base}.{counter}"
        return username

    @transaction.atomic
    def save(self, commit=True):
        user = forms.ModelForm.save(self, commit=False)
        if hasattr(self, "generated_username"):
            user.username = self.generated_username
        user.email = self.cleaned_data.get("email", "")
        user.is_active = self.cleaned_data.get("is_active", True)
        user.set_password(settings.DEFAULT_INITIAL_PASSWORD)
        if commit:
            user.save()
            user.groups.set(self.cleaned_data.get("groups"))
        empleado_email = self.cleaned_data.get("email_empleado") or user.email
        Empleado.objects.create(
            user=user,
            nombres=self.cleaned_data.get("nombres"),
            apellidos=self.cleaned_data.get("apellidos"),
            curp=self.cleaned_data.get("curp", ""),
            rfc=self.cleaned_data.get("rfc", ""),
            telefono=self.cleaned_data.get("telefono", ""),
            email=empleado_email or "",
            direccion=self.cleaned_data.get("direccion", ""),
            fecha_nacimiento=self.cleaned_data.get("fecha_nacimiento"),
            fecha_ingreso=self.cleaned_data.get("fecha_ingreso"),
            puesto=self.cleaned_data.get("puesto"),
            turno_preferido=self.cleaned_data.get("turno_preferido"),
            estatus=self.cleaned_data.get("estatus"),
            foto=self.cleaned_data.get("foto"),
            notas=self.cleaned_data.get("notas", ""),
        )
        return user
