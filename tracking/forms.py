from django import forms

from .models import Dispositivo, PermisoGPS, Ubicacion


class BaseBootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                continue
            css_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css_class + " form-control").strip()


class DispositivoForm(BaseBootstrapForm):
    class Meta:
        model = Dispositivo
        fields = "__all__"


class PermisoGPSForm(BaseBootstrapForm):
    class Meta:
        model = PermisoGPS
        fields = "__all__"


class UbicacionForm(BaseBootstrapForm):
    class Meta:
        model = Ubicacion
        fields = "__all__"

    def clean_latitud(self):
        lat = self.cleaned_data.get("latitud")
        if lat is not None and (lat < -90 or lat > 90):
            raise forms.ValidationError("Latitud fuera de rango.")
        return lat

    def clean_longitud(self):
        lon = self.cleaned_data.get("longitud")
        if lon is not None and (lon < -180 or lon > 180):
            raise forms.ValidationError("Longitud fuera de rango.")
        return lon

    def clean_bateria(self):
        bateria = self.cleaned_data.get("bateria")
        if bateria is not None and (bateria < 0 or bateria > 100):
            raise forms.ValidationError("Bateria fuera de rango (0-100).")
        return bateria
