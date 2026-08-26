from django import forms

from .models import Animal


class AnimalEditForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = (
            "numero_arete",
            "nombre_propio",
            "sexo",
            "categoria",
            "estado",
            "especie",
            "raza_declarada",
            "fecha_nacimiento",
            "padre",
            "madre",
            "microchip",
            "tatuaje",
            "registro_genealogico",
            "observaciones",
            "is_active",
        )
        widgets = {
            "numero_arete": forms.TextInput(attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-blue-500 focus:border-blue-500"}),
            "nombre_propio": forms.TextInput(attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-blue-500 focus:border-blue-500"}),
            "sexo": forms.Select(attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-gray-50"}),
            "categoria": forms.TextInput(attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-blue-500 focus:border-blue-500"}),
            "estado": forms.Select(attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2 font-semibold", "id": "id_estado"}),
            "especie": forms.Select(attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-gray-50", "id": "id_especie"}),
            "raza_declarada": forms.Select(attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-gray-50"}),
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date", "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-blue-500 focus:border-blue-500"}),
            "padre": forms.Select(attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2 text-gray-700"}),
            "madre": forms.Select(attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2 text-gray-700"}),
            "microchip": forms.TextInput(attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-blue-500 focus:border-blue-500"}),
            "tatuaje": forms.TextInput(attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-blue-500 focus:border-blue-500"}),
            "registro_genealogico": forms.TextInput(attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-blue-500 focus:border-blue-500"}),
            "observaciones": forms.Textarea(attrs={"rows": 5, "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-blue-500 focus:border-blue-500 text-sm"}),
            "is_active": forms.CheckboxInput(attrs={"class": "w-5 h-5 text-blue-600 rounded focus:ring-blue-500 border-gray-300", "id": "id_is_active"}),
        }

    def __init__(self, *args, finca=None, **kwargs):
        self.finca = finca
        super().__init__(*args, **kwargs)

        base = (
            Animal.objects
            .filter(finca=finca)
            .exclude(pk=self.instance.pk)
            .select_related("especie")
        ) if finca is not None else Animal.objects.none()

        especie_id = None
        if self.is_bound:
            especie_id = self.data.get(self.add_prefix("especie"))
        if not especie_id:
            especie_id = self.instance.especie_id

        if especie_id:
            base = base.filter(especie_id=especie_id)

        self.fields["padre"].queryset = base.filter(sexo="M").order_by("numero_arete")
        self.fields["madre"].queryset = base.filter(sexo="H").order_by("numero_arete")

    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get("estado")
        especie = cleaned_data.get("especie")
        padre = cleaned_data.get("padre")
        madre = cleaned_data.get("madre")

        if padre and especie and padre.especie_id != especie.id:
            self.add_error("padre", "El padre debe pertenecer a la misma especie.")
        if madre and especie and madre.especie_id != especie.id:
            self.add_error("madre", "La madre debe pertenecer a la misma especie.")

        if estado in {"vendido", "muerto", "descartado", "trasladado"}:
            cleaned_data["is_active"] = False

        return cleaned_data
