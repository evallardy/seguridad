from django import forms

from .models import CentroCosto, Cuenta, Factura, Movimiento, RelacionCentroCosto


class BaseBootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                continue
            css_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css_class + " form-control").strip()


class CuentaForm(BaseBootstrapForm):
    class Meta:
        model = Cuenta
        fields = "__all__"


class CentroCostoForm(BaseBootstrapForm):
    class Meta:
        model = CentroCosto
        fields = "__all__"


class MovimientoForm(BaseBootstrapForm):
    class Meta:
        model = Movimiento
        fields = "__all__"

    def clean_monto(self):
        monto = self.cleaned_data.get("monto")
        if monto is not None and monto <= 0:
            raise forms.ValidationError("El monto debe ser mayor a cero.")
        return monto


class RelacionCentroCostoForm(BaseBootstrapForm):
    class Meta:
        model = RelacionCentroCosto
        fields = "__all__"


class FacturaForm(BaseBootstrapForm):
    class Meta:
        model = Factura
        fields = "__all__"

    def clean(self):
        cleaned = super().clean()
        subtotal = cleaned.get("subtotal") or 0
        impuestos = cleaned.get("impuestos") or 0
        total = cleaned.get("total") or 0
        if total < subtotal + impuestos:
            self.add_error("total", "El total no puede ser menor que subtotal + impuestos.")
        return cleaned
