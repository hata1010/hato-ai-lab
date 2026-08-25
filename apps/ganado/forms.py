from django import forms
from django.utils import timezone

from .models import Animal, PesajeAnimal


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


class PesajeAnimalForm(forms.ModelForm):
    class Meta:
        model = PesajeAnimal
        fields = ("animal", "fecha", "peso_kg", "observaciones")
        widgets = {
            "fecha": forms.DateTimeInput(format="%Y-%m-%dT%H:%M", attrs={"type": "datetime-local"}),
            "peso_kg": forms.NumberInput(attrs={"step": "0.01", "min": "0.01", "inputmode": "decimal"}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, finca=None, animal=None, **kwargs):
        self.finca = finca
        super().__init__(*args, **kwargs)
        self.fields["fecha"].input_formats = ["%Y-%m-%dT%H:%M"]
        queryset = Animal.objects.filter(finca=finca).order_by("numero_arete") if finca is not None else Animal.objects.none()
        self.fields["animal"].queryset = queryset
        if animal is not None:
            if finca is None or animal.finca_id != finca.id:
                self.fields["animal"].queryset = Animal.objects.none()
            else:
                self.fields["animal"].initial = animal
        if not self.instance.pk and not self.initial.get("fecha"):
            self.initial["fecha"] = timezone.localtime().strftime("%Y-%m-%dT%H:%M")

    def clean_animal(self):
        animal = self.cleaned_data["animal"]
        if self.finca is not None and animal.finca_id != self.finca.id:
            raise forms.ValidationError("El animal debe pertenecer a la finca activa.")
        return animal
