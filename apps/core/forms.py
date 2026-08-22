from django import forms
from django.contrib.gis.geos import GEOSGeometry

from .models import Potrero


class PotreroForm(forms.ModelForm):
    ubicacion_wkt = forms.CharField(
        required=False,
        label="Ubicación (WKT)",
        help_text="Opcional. Ejemplo: POINT(-67.4 8.9)",
        widget=forms.TextInput(attrs={"placeholder": "POINT(-67.4 8.9)"}),
    )
    poligono_wkt = forms.CharField(
        required=False,
        label="Polígono (WKT)",
        help_text="Opcional. Ejemplo: POLYGON((-67.4 8.9,-67.39 8.9,-67.39 8.91,-67.4 8.91,-67.4 8.9))",
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "POLYGON((...))"}),
    )

    class Meta:
        model = Potrero
        fields = [
            "nombre",
            "codigo",
            "tipo",
            "area_hectareas",
            "capacidad_animales",
            "carga_actual",
            "tipo_pasto",
            "calidad_pasto",
            "estado",
            "dias_descanso",
            "fecha_ultimo_pastoreo",
            "descripcion",
            "is_active",
        ]
        widgets = {
            "fecha_ultimo_pastoreo": forms.DateInput(attrs={"type": "date"}),
            "descripcion": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, potrero=None, **kwargs):
        super().__init__(*args, **kwargs)
        if potrero:
            if potrero.ubicacion:
                self.fields["ubicacion_wkt"].initial = potrero.ubicacion.wkt
            if potrero.poligono:
                self.fields["poligono_wkt"].initial = potrero.poligono.wkt

    def _geometry(self, field_name, geometry_type):
        value = self.cleaned_data.get(field_name, "").strip()
        if not value:
            return None
        try:
            geometry = GEOSGeometry(value, srid=4326)
        except Exception as exc:
            raise forms.ValidationError(f"Geometría inválida: {exc}")
        if geometry.geom_type.upper() != geometry_type:
            raise forms.ValidationError(
                f"Se esperaba una geometría {geometry_type}, no {geometry.geom_type.upper()}."
            )
        return geometry

    def clean_ubicacion_wkt(self):
        return self._geometry("ubicacion_wkt", "POINT")

    def clean_poligono_wkt(self):
        return self._geometry("poligono_wkt", "POLYGON")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.ubicacion = self.cleaned_data.get("ubicacion_wkt")
        instance.poligono = self.cleaned_data.get("poligono_wkt")
        if commit:
            instance.save()
        return instance
