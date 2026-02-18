from django import forms

from .models import DetalleMantenimiento, Inspeccion, OrdenMantenimiento, ProgramacionMantenimiento


class BaseBootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                continue
            css_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css_class + " form-control").strip()


class OrdenMantenimientoForm(BaseBootstrapForm):
    class Meta:
        model = OrdenMantenimiento
        fields = "__all__"

    def clean(self):
        cleaned = super().clean()
        fecha_apertura = cleaned.get("fecha_apertura")
        fecha_cierre = cleaned.get("fecha_cierre")
        if fecha_apertura and fecha_cierre and fecha_cierre < fecha_apertura:
            self.add_error("fecha_cierre", "La fecha cierre no puede ser menor a la fecha apertura.")
        return cleaned


class DetalleMantenimientoForm(BaseBootstrapForm):
    class Meta:
        model = DetalleMantenimiento
        fields = "__all__"


class ProgramacionMantenimientoForm(BaseBootstrapForm):
    class Meta:
        model = ProgramacionMantenimiento
        fields = "__all__"


class InspeccionForm(BaseBootstrapForm):
    class Meta:
        model = Inspeccion
        fields = "__all__"
