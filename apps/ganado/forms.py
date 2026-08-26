from django import forms
from django.utils import timezone

from apps.core.models import Potrero

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

        animales = Animal.objects.filter(finca=finca).order_by("numero_arete") if finca is not None else Animal.objects.none()
        self.fields["padre"].queryset = animales.filter(sexo="M")
        self.fields["madre"].queryset = animales.filter(sexo="H")

    def clean(self):
        cleaned = super().clean()
        if self.finca is not None:
            self.instance.finca = self.finca
        return cleaned


class IngresoAnimalForm(forms.ModelForm):
    ORIGEN_CHOICES = (
        ("compra", "Compra"),
        ("nacimiento_granja", "Nacimiento en la finca"),
    )

    origen = forms.ChoiceField(
        choices=ORIGEN_CHOICES,
        widget=forms.RadioSelect,
        initial="compra",
        label="¿Cómo ingresa el animal?",
    )
    padre = forms.ModelChoiceField(
        queryset=Animal.objects.none(),
        required=False,
        empty_label="Sin padre registrado",
        label="Padre (toro)",
    )
    madre = forms.ModelChoiceField(
        queryset=Animal.objects.none(),
        required=False,
        empty_label="Sin madre registrada",
        label="Madre (vaca)",
    )
    potrero_inicial = forms.ModelChoiceField(
        queryset=Potrero.objects.none(),
        required=False,
        empty_label="Sin ubicación inicial",
        label="Ubicación inicial",
    )
    peso_inicial = forms.DecimalField(
        required=False,
        min_value=0.01,
        max_digits=7,
        decimal_places=2,
        label="Peso inicial (kg)",
    )
    proveedor = forms.CharField(max_length=200, required=False, label="Proveedor")
    fecha_compra = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Fecha de compra",
    )
    documento_compra = forms.CharField(
        max_length=100,
        required=False,
        label="Factura / Documento",
    )
    precio_individual = forms.DecimalField(
        required=False,
        min_value=0,
        max_digits=14,
        decimal_places=2,
        label="Precio individual",
    )
    fecha_parto = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        label="Fecha y hora del parto",
    )
    tipo_parto = forms.ChoiceField(
        required=False,
        choices=(
            ("normal", "Normal"),
            ("distocico", "Distócico"),
            ("cesarea", "Cesárea"),
        ),
        label="Tipo de parto",
    )

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
        animales = Animal.objects.filter(finca=finca).order_by("numero_arete") if finca is not None else Animal.objects.none()
        self.fields["padre"].queryset = animales.filter(sexo="M")
        self.fields["madre"].queryset = animales.filter(sexo="H")
        self.fields["potrero_inicial"].queryset = (
            Potrero.objects.filter(finca=finca, is_active=True).order_by("nombre")
            if finca is not None else Potrero.objects.none()
        )

    def clean(self):
        cleaned = super().clean()
        origen = cleaned.get("origen")
        especie = cleaned.get("especie")
        padre = cleaned.get("padre")
        madre = cleaned.get("madre")

        if self.finca is not None:
            self.instance.finca = self.finca

        if padre and especie and padre.especie_id != especie.id:
            self.add_error("padre", "El padre debe pertenecer a la misma especie.")
        if madre and especie and madre.especie_id != especie.id:
            self.add_error("madre", "La madre debe pertenecer a la misma especie.")

        if origen == "nacimiento_granja":
            if not madre:
                self.add_error("madre", "Un nacimiento en la finca requiere identificar la madre.")
            if not cleaned.get("fecha_parto"):
                self.add_error("fecha_parto", "El nacimiento requiere la fecha del parto.")
            if not cleaned.get("tipo_parto"):
                self.add_error("tipo_parto", "El nacimiento requiere el tipo de parto.")
        elif origen == "compra":
            if not cleaned.get("proveedor"):
                self.add_error("proveedor", "La compra requiere proveedor.")
            if not cleaned.get("fecha_compra"):
                self.add_error("fecha_compra", "La compra requiere fecha.")

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
