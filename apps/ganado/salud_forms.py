from django import forms

from .models import Animal, EventoSalud


class EventoSaludForm(forms.ModelForm):
    class Meta:
        model = EventoSalud
        fields = (
            "animal",
            "tipo",
            "fecha",
            "producto",
            "dosis",
            "nombre_veterinario",
            "observaciones",
        )
        widgets = {
            "fecha": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local"},
            ),
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
        if self.finca is not None and animal is not None and animal.finca_id != self.finca.id:
            self.add_error("animal", "El animal debe pertenecer a la finca activa.")
        if self.instance.pk and self.finca is not None:
            self.instance.animal_id = self.instance.animal_id
        return cleaned
