from django.contrib import admin

from .models_reproduccion import (
    EventoReproductivo,
    CriaNacimiento,
    Lactancia,
    ControlLeche,
)


@admin.register(EventoReproductivo)
class EventoReproductivoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "finca",
        "animal",
        "tipo_evento",
        "fecha",
        "metodo_reproductivo",
        "toro",
        "semen_codigo",
        "resultado_gestacion",
        "tipo_parto",
    )
    list_filter = (
        "finca",
        "tipo_evento",
        "metodo_reproductivo",
        "resultado_gestacion",
        "tipo_parto",
    )
    search_fields = (
        "animal__numero_arete",
        "animal__nombre_propio",
        "toro__numero_arete",
        "semen_codigo",
    )
    autocomplete_fields = ("finca", "animal", "toro", "creado_por")
    date_hierarchy = "fecha"
    ordering = ("-fecha",)


@admin.register(CriaNacimiento)
class CriaNacimientoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "finca",
        "parto",
        "animal",
        "creado_por",
    )
    list_filter = ("finca",)
    search_fields = (
        "parto__animal__numero_arete",
        "animal__numero_arete",
        "animal__nombre_propio",
    )
    autocomplete_fields = ("finca", "parto", "animal", "creado_por")


@admin.register(Lactancia)
class LactanciaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "finca",
        "animal",
        "numero_lactancia",
        "fecha_inicio",
        "fecha_secado",
        "estado",
        "parto_origen",
    )
    list_filter = ("finca", "estado", "fecha_inicio")
    search_fields = (
        "animal__numero_arete",
        "animal__nombre_propio",
    )
    autocomplete_fields = ("finca", "animal", "parto_origen", "creado_por")
    date_hierarchy = "fecha_inicio"
    ordering = ("-fecha_inicio",)


@admin.register(ControlLeche)
class ControlLecheAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "finca",
        "lactancia",
        "fecha",
        "jornada",
        "cantidad",
        "unidad",
        "creado_por",
    )
    list_filter = ("finca", "jornada", "unidad", "fecha")
    search_fields = (
        "lactancia__animal__numero_arete",
        "lactancia__animal__nombre_propio",
    )
    autocomplete_fields = ("finca", "lactancia", "creado_por")
    date_hierarchy = "fecha"
    ordering = ("-fecha",)
