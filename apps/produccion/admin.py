from django.contrib import admin

from .models import Metrica, VariableMetrica


# ============================================================
# VARIABLES DE LA MÉTRICA
# ============================================================

class VariableMetricaInline(admin.TabularInline):

    model = VariableMetrica

    extra = 0

    fields = (
        "codigo",
        "nombre",
        "tipo",
        "fuente",
        "campo",
        "regla",
        "orden",
        "activa",
    )


# ============================================================
# MÉTRICA
# ============================================================

@admin.register(Metrica)
class MetricaAdmin(admin.ModelAdmin):

    list_display = (
        "finca",
        "codigo",
        "nombre",
        "categoria",
        "unidad_resultado",
        "periodicidad",
        "tipo_resultado",
        "activa",
        "version",
    )

    list_filter = (
        "finca",
        "categoria",
        "periodicidad",
        "tipo_resultado",
        "activa",
    )

    search_fields = (
        "codigo",
        "nombre",
        "descripcion",
        "formula",
        "finca__nombre",
    )

    ordering = (
        "finca",
        "categoria",
        "nombre",
    )

    # ========================================================
    # FORMULARIO
    # ========================================================

    fieldsets = (
        (
            "Identificación",
            {
                "fields": (
                    "finca",
                    "nombre",
                    "codigo",
                    "descripcion",
                )
            },
        ),

        (
            "Clasificación",
            {
                "fields": (
                    "categoria",
                    "unidad_resultado",
                    "periodicidad",
                    "tipo_resultado",
                )
            },
        ),

        (
            "Definición del cálculo",
            {
                "fields": (
                    "formula",
                ),
                "description": (
                    "Escriba la expresión que define "
                    "el cálculo de la métrica. "
                    "Ejemplo: "
                    "(PESO_FINAL - PESO_INICIAL) / DIAS"
                ),
            },
        ),

        (
            "Control",
            {
                "fields": (
                    "activa",
                    "version",
                )
            },
        ),

        (
            "Auditoría",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    # ========================================================
    # VARIABLES
    # ========================================================

    inlines = [
        VariableMetricaInline,
    ]


# ============================================================
# ADMINISTRACIÓN DIRECTA DE VARIABLES
# ============================================================

@admin.register(VariableMetrica)
class VariableMetricaAdmin(admin.ModelAdmin):

    list_display = (
        "metrica",
        "finca",
        "codigo",
        "nombre",
        "tipo",
        "fuente",
        "campo",
        "regla",
        "orden",
        "activa",
    )

    list_filter = (
        "metrica__finca",
        "tipo",
        "regla",
        "activa",
    )

    search_fields = (
        "codigo",
        "nombre",
        "fuente",
        "campo",
        "metrica__codigo",
        "metrica__nombre",
        "metrica__finca__nombre",
    )

    ordering = (
        "metrica__finca",
        "metrica",
        "orden",
        "codigo",
    )

    @admin.display(
        description="Finca",
        ordering="metrica__finca__nombre",
    )
    def finca(self, obj):
        return obj.metrica.finca

