from django import forms

from .models import Animal, MovimientoAnimal
from apps.core.models import Potrero


class MovimientoAnimalForm(forms.ModelForm):
    class Meta:
        model = MovimientoAnimal
        fields = ("animal", "potrero", "fecha_entrada", "observaciones")
        widgets = {
            "fecha_entrada": forms.DateTimeInput(format="%Y-%m-%dT%H:%M", attrs={"type": "datetime-local"}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, finca=None, **kwargs):
        self.finca = finca
        super().__init__(*args, **kwargs)
        self.fields["animal"].queryset = (
            Animal.objects.filter(finca=finca).order_by("numero_arete")
            if finca is not None else Animal.objects.none()
        )
        self.fields["potrero"].queryset = (
            Potrero.objects.filter(finca=finca, is_active=True).order_by("nombre")
            if finca is not None else Potrero.objects.none()
        )
        self.fields["fecha_entrada"].input_formats = ["%Y-%m-%dT%H:%M"]

    def clean(self):
        cleaned = super().clean()
        animal = cleaned.get("animal")
        potrero = cleaned.get("potrero")
        if self.finca is not None:
            if animal is not None and animal.finca_id != self.finca.id:
                self.add_error("animal", "El animal debe pertenecer a la finca activa.")
            if potrero is not None and potrero.finca_id != self.finca.id:
                self.add_error("potrero", "El potrero debe pertenecer a la finca activa.")
            if animal is not None and MovimientoAnimal.objects.filter(animal=animal, activo=True).exclude(pk=self.instance.pk).exists():
                self.add_error("animal", "El animal ya tiene un movimiento activo. Debe cerrarse antes de registrarlo en otro potrero.")
        return cleaned


class CambioPotreroForm(forms.Form):
    potrero = forms.ModelChoiceField(queryset=Potrero.objects.none(), label="Nuevo potrero")
    fecha_entrada = forms.DateTimeField(
        label="Fecha y hora del cambio",
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(format="%Y-%m-%dT%H:%M", attrs={"type": "datetime-local"}),
    )
    observaciones = forms.CharField(
        label="Observaciones",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )

    def __init__(self, *args, finca=None, potrero_actual=None, **kwargs):
        self.finca = finca
        self.potrero_actual = potrero_actual
        super().__init__(*args, **kwargs)
        self.fields["potrero"].queryset = (
            Potrero.objects.filter(finca=finca, is_active=True).order_by("nombre")
            if finca is not None else Potrero.objects.none()
        )

    def clean_potrero(self):
        potrero = self.cleaned_data["potrero"]
        if self.finca is not None and potrero.finca_id != self.finca.id:
            raise forms.ValidationError("El nuevo potrero debe pertenecer a la finca activa.")
        if self.potrero_actual is not None and potrero.pk == self.potrero_actual.pk:
            raise forms.ValidationError("El nuevo potrero debe ser diferente al potrero actual.")
        return potrero
