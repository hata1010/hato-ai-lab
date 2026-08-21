from django import forms

from .models import Animal, PesajeAnimal


class PesajeAnimalForm(forms.ModelForm):
    class Meta:
        model = PesajeAnimal
        fields = ("animal", "fecha", "peso_kg", "observaciones")
        widgets = {
            "fecha": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local"},
            ),
            "peso_kg": forms.NumberInput(attrs={"step": "0.01", "min": "0.01"}),
            "observaciones": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, finca=None, **kwargs):
        self.finca = finca
        super().__init__(*args, **kwargs)
        self.fields["animal"].queryset = (
            Animal.objects.filter(finca=finca).order_by("numero_arete")
            if finca is not None
            else Animal.objects.none()
        )
        self.fields["fecha"].input_formats = ["%Y-%m-%dT%H:%M"]

    def clean(self):
        cleaned = super().clean()
        animal = cleaned.get("animal")
        peso = cleaned.get("peso_kg")
        if self.finca is not None and animal is not None and animal.finca_id != self.finca.id:
            self.add_error("animal", "El animal debe pertenecer a la finca activa.")
        if peso is not None and peso <= 0:
            self.add_error("peso_kg", "El peso debe ser mayor que cero.")
        return cleaned
