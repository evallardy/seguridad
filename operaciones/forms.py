from django import forms

from .models import Cliente, Contrato, Servicio, Sitio


class BaseBootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                continue
            css_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css_class + " form-control").strip()


class ClienteForm(BaseBootstrapForm):
    class Meta:
        model = Cliente
        fields = "__all__"


class SitioForm(BaseBootstrapForm):
    class Meta:
        model = Sitio
        fields = "__all__"


class ServicioForm(BaseBootstrapForm):
    class Meta:
        model = Servicio
        fields = "__all__"


class ContratoForm(BaseBootstrapForm):
    class Meta:
        model = Contrato
        fields = "__all__"

    def clean(self):
        cleaned = super().clean()
        fecha_inicio = cleaned.get("fecha_inicio")
        fecha_fin = cleaned.get("fecha_fin")
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            self.add_error("fecha_fin", "La fecha fin no puede ser menor a la fecha inicio.")
        return cleaned
