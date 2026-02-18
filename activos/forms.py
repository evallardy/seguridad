from django import forms

from .models import Armamento, AsignacionActivo, Refaccion, RegistroCombustible, Vehiculo


class BaseBootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                continue
            css_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css_class + " form-control").strip()


class VehiculoForm(BaseBootstrapForm):
    class Meta:
        model = Vehiculo
        fields = "__all__"


class ArmamentoForm(BaseBootstrapForm):
    class Meta:
        model = Armamento
        fields = "__all__"


class RefaccionForm(BaseBootstrapForm):
    class Meta:
        model = Refaccion
        fields = "__all__"


class AsignacionActivoForm(BaseBootstrapForm):
    class Meta:
        model = AsignacionActivo
        fields = "__all__"
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"type": "date"}),
        }


class RegistroCombustibleForm(BaseBootstrapForm):
    class Meta:
        model = RegistroCombustible
        fields = "__all__"
        widgets = {
            "fecha": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
