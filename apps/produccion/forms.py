"""Formularios para la administración de definiciones de métricas en Hato V1."""

from django import forms
from apps.produccion.models import Metrica
from apps.produccion.engine.catalogo_v1 import METRICAS_V1

# Opciones de cálculo basadas en el catálogo oficial V1
CODIGO_CALCULO_CHOICES = [
    (m.codigo, f"{m.nombre} ({m.codigo}) — {m.unidad}")
    for m in METRICAS_V1.values()
]


class MetricaForm(forms.ModelForm):
    codigo = forms.ChoiceField(
        choices=CODIGO_CALCULO_CHOICES,
        label="Motor de Cálculo (Catálogo V1)",
        help_text="Seleccione la fórmula/motor del catálogo oficial V1 que ejecutará esta métrica.",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Metrica
        fields = [
            "nombre",
            "codigo",
            "categoria",
            "unidad_resultado",
            "periodicidad",
            "tipo_resultado",
            "descripcion",
            "activa",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. Ganancia Media Diaria Lote Ceba"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "unidad_resultado": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. kg/día, cab/ha, animales"}),
            "periodicidad": forms.Select(attrs={"class": "form-select"}),
            "tipo_resultado": forms.Select(attrs={"class": "form-select"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Describa el objetivo zootécnico o productivo de esta métrica."}),
            "activa": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si ya existe y el código no está en choices estándar, permitirlo como opción
        if self.instance and self.instance.pk and self.instance.codigo:
            codigos_actuales = [c[0] for c in CODIGO_CALCULO_CHOICES]
            if self.instance.codigo not in codigos_actuales:
                self.fields["codigo"].choices = [(self.instance.codigo, self.instance.codigo)] + CODIGO_CALCULO_CHOICES
