from django import forms

from .models import Animal


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
        if self.finca is not None:
            self.instance.finca = self.finca
        return cleaned
