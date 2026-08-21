from django import forms

from .models import Animal
from apps.core.tenant import obtener_finca_activa


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = (
            "numero_arete",
            "nombre_propio",
            "fecha_nacimiento",
            "sexo",
            "especie",
            "raza_declarada",
            "categoria",
            "microchip",
            "tatuaje",
            "registro_genealogico",
            "padre",
            "madre",
            "estado",
            "observaciones",
            "is_active",
        )
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, finca=None, **kwargs):
        self.finca = finca
        super().__init__(*args, **kwargs)

        if finca is not None:
            self.fields["padre"].queryset = Animal.objects.filter(finca=finca).order_by("numero_arete")
            self.fields["madre"].queryset = Animal.objects.filter(finca=finca).order_by("numero_arete")
        else:
            self.fields["padre"].queryset = Animal.objects.none()
            self.fields["madre"].queryset = Animal.objects.none()

    def clean(self):
        cleaned = super().clean()
        instance = self.instance
        if self.finca is not None:
            instance.finca = self.finca
        instance.__dict__.update({k: v for k, v in cleaned.items() if k in self.fields})
        if self.finca is not None:
            instance.finca = self.finca
        self.instance = instance
        return cleaned
