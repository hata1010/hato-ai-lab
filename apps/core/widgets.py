# app/apps/core/widgets.py
from django import forms

class LatLonWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.TextInput(attrs={'placeholder': 'Latitud', 'style': 'width:45%'}),
            forms.TextInput(attrs={'placeholder': 'Longitud', 'style': 'width:45%'}),
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.latitud, value.longitud]
        return [None, None]