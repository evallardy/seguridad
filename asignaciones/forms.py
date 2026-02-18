from django import forms

from .models import Asignacion, AsignacionEmpleado, Equipo, Ruta, RutaPunto


class BaseBootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                continue
            css_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css_class + " form-control").strip()


class RutaForm(BaseBootstrapForm):
    class Meta:
        model = Ruta
        fields = ("nombre", "descripcion", "estatus")


class EquipoForm(BaseBootstrapForm):
    class Meta:
        model = Equipo
        fields = "__all__"


class RutaPuntoForm(BaseBootstrapForm):
    class Meta:
        model = RutaPunto
        fields = ("orden", "nombre", "km_desde_anterior")


class AsignacionForm(BaseBootstrapForm):
    class Meta:
        model = Asignacion
        fields = "__all__"
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned = super().clean()
        tipo = cleaned.get("tipo")
        sitio = cleaned.get("sitio")
        ruta = cleaned.get("ruta")
        fecha_inicio = cleaned.get("fecha_inicio")
        fecha_fin = cleaned.get("fecha_fin")

        if tipo == "ruta" and not ruta:
            self.add_error("ruta", "Selecciona una ruta para asignaciones de tipo ruta.")
        if tipo == "sitio" and not sitio:
            self.add_error("sitio", "Selecciona un sitio para asignaciones de tipo sitio.")
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            self.add_error("fecha_fin", "La fecha fin no puede ser menor a la fecha inicio.")
        return cleaned


class AsignacionEmpleadoForm(BaseBootstrapForm):
    class Meta:
        model = AsignacionEmpleado
        fields = "__all__"
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned = super().clean()
        fecha_inicio = cleaned.get("fecha_inicio")
        fecha_fin = cleaned.get("fecha_fin")
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            self.add_error("fecha_fin", "La fecha fin no puede ser menor a la fecha inicio.")
        return cleaned
