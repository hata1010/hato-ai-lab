from django.contrib import admin

from .models import (
    Especie,
    Raza,
    TipoPasto,
    Animal,
    ProcedenciaAnimal,
    Adquisicion,
    AdquisicionAnimal,
    ComposicionGenetica,
    DocumentoAnimal,
    MovimientoAnimal,
    PesajeAnimal,
    EventoSalud,
)


# ============================================================
# ESPECIE
# ============================================================

@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nombre",
        "descripcion",
    )

    search_fields = (
        "nombre",
    )

    ordering = (
        "nombre",
    )


# ============================================================
# RAZA
# ============================================================

@admin.register(Raza)
class RazaAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nombre",
        "especie",
    )

    list_filter = (
        "especie",
    )

    search_fields = (
        "nombre",
        "especie__nombre",
    )

    autocomplete_fields = (
        "especie",
    )

    ordering = (
        "especie",
        "nombre",
    )


# ============================================================
# TIPO DE PASTO
# ============================================================

@admin.register(TipoPasto)
class TipoPastoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nombre",
        "descripcion",
    )

    search_fields = (
        "nombre",
    )

    ordering = (
        "nombre",
    )


# ============================================================
# INLINE — COMPOSICIÓN GENÉTICA
# ============================================================

class ComposicionGeneticaInline(admin.TabularInline):

    model = ComposicionGenetica

    extra = 1

    fields = (
        "raza",
        "porcentaje",
        "metodo",
        "confiabilidad",
        "fecha_verificacion",
        "observaciones",
    )

    autocomplete_fields = (
        "raza",
    )


# ============================================================
# INLINE — DOCUMENTOS
# ============================================================

class DocumentoAnimalInline(admin.TabularInline):

    model = DocumentoAnimal

    extra = 0

    fields = (
        "tipo",
        "numero_documento",
        "fecha_documento",
        "archivo",
        "observaciones",
    )


# ============================================================
# INLINE — PROCEDENCIA
# ============================================================

class ProcedenciaAnimalInline(admin.StackedInline):

    model = ProcedenciaAnimal

    extra = 0

    max_num = 1

    fields = (
        "tipo",
        "fecha",
        "origen_nombre",
        "origen_identificacion",
        "observaciones",
    )


# ============================================================
# INLINE — ADQUISICIÓN
# ============================================================

class AdquisicionAnimalInline(admin.StackedInline):

    model = AdquisicionAnimal

    extra = 0

    max_num = 1

    fields = (
        "adquisicion",
        "precio_individual",
        "observaciones",
    )

    autocomplete_fields = (
        "adquisicion",
    )


# ============================================================
# INLINE — MOVIMIENTOS
# ============================================================

class MovimientoAnimalInline(admin.TabularInline):

    model = MovimientoAnimal

    extra = 0

    fields = (
        "potrero",
        "tipo_pasto",
        "fecha_entrada",
        "fecha_salida",
        "activo",
        "observaciones",
    )

    autocomplete_fields = (
        "potrero",
        "tipo_pasto",
    )

    ordering = (
        "-fecha_entrada",
    )


# ============================================================
# INLINE — PESAJE
# ============================================================

class PesajeAnimalInline(admin.TabularInline):

    model = PesajeAnimal

    extra = 1

    fields = (
        "fecha",
        "peso_kg",
        "observaciones",
    )

    ordering = (
        "-fecha",
    )


# ============================================================
# INLINE — EVENTOS DE SALUD
# ============================================================

class EventoSaludInline(admin.TabularInline):

    model = EventoSalud

    extra = 0

    fields = (
        "tipo",
        "fecha",
        "producto",
        "dosis",
        "nombre_veterinario",
        "observaciones",
    )

    ordering = (
        "-fecha",
    )


# ============================================================
# ANIMAL
# ============================================================

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "numero_arete",
        "nombre_propio",
        "especie",
        "raza_declarada",
        "sexo",
        "categoria",
        "estado",
        "padre",
        "madre",
    )

    list_filter = (
        "especie",
        "raza_declarada",
        "sexo",
        "categoria",
        "estado",
        "is_active",
    )

    search_fields = (
        "numero_arete",
        "nombre_propio",
        "microchip",
        "tatuaje",
        "registro_genealogico",
        "padre__numero_arete",
        "madre__numero_arete",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "padre",
        "madre",
        "especie",
        "raza_declarada",
    )

    fieldsets = (

        # ----------------------------------------------------
        # IDENTIDAD
        # ----------------------------------------------------

        (
            "🐄 Identidad del animal",
            {
                "fields": (
                    "numero_arete",
                    "nombre_propio",
                    "fecha_nacimiento",
                    "sexo",
                    "especie",
                    "raza_declarada",
                    "categoria",
                )
            },
        ),

        # ----------------------------------------------------
        # IDENTIFICACIÓN
        # ----------------------------------------------------

        (
            "🏷️ Identificación adicional",
            {
                "fields": (
                    "microchip",
                    "tatuaje",
                    "registro_genealogico",
                )
            },
        ),

        # ----------------------------------------------------
        # GENEALOGÍA
        # ----------------------------------------------------

        (
            "🧬 Genealogía",
            {
                "fields": (
                    "padre",
                    "madre",
                ),
                "description": (
                    "Los padres pueden ser animales registrados "
                    "en esta finca. La composición genética y "
                    "documentación permiten registrar información "
                    "genética externa."
                ),
            },
        ),

        # ----------------------------------------------------
        # ESTADO
        # ----------------------------------------------------

        (
            "📌 Estado",
            {
                "fields": (
                    "estado",
                    "is_active",
                    "observaciones",
                )
            },
        ),

        # ----------------------------------------------------
        # AUDITORÍA
        # ----------------------------------------------------

        (
            "🔐 Auditoría",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    inlines = (
        ProcedenciaAnimalInline,
        ComposicionGeneticaInline,
        DocumentoAnimalInline,
        AdquisicionAnimalInline,
        MovimientoAnimalInline,
        PesajeAnimalInline,
        EventoSaludInline,
    )

    ordering = (
        "numero_arete",
    )


# ============================================================
# ADQUISICIÓN
# ============================================================

class AdquisicionAnimalInlineForAdquisicion(admin.TabularInline):

    model = AdquisicionAnimal

    extra = 1

    fields = (
        "animal",
        "precio_individual",
        "observaciones",
    )

    autocomplete_fields = (
        "animal",
    )


@admin.register(Adquisicion)
class AdquisicionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "numero_documento",
        "proveedor",
        "fecha",
        "costo_total",
    )

    list_filter = (
        "fecha",
    )

    search_fields = (
        "numero_documento",
        "proveedor",
    )

    date_hierarchy = "fecha"

    fieldsets = (
        (
            "📄 Documento de adquisición",
            {
                "fields": (
                    "proveedor",
                    "fecha",
                    "numero_documento",
                    "costo_total",
                    "observaciones",
                )
            },
        ),
    )

    inlines = (
        AdquisicionAnimalInlineForAdquisicion,
    )

    ordering = (
        "-fecha",
    )


# ============================================================
# ADQUISICIÓN — RELACIÓN ANIMAL
# ============================================================

@admin.register(AdquisicionAnimal)
class AdquisicionAnimalAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "adquisicion",
        "animal",
        "precio_individual",
    )

    list_filter = (
        "adquisicion__fecha",
    )

    search_fields = (
        "animal__numero_arete",
        "animal__nombre_propio",
        "adquisicion__numero_documento",
        "adquisicion__proveedor",
    )

    autocomplete_fields = (
        "animal",
        "adquisicion",
    )


# ============================================================
# PROCEDENCIA
# ============================================================

@admin.register(ProcedenciaAnimal)
class ProcedenciaAnimalAdmin(admin.ModelAdmin):

    list_display = (
        "animal",
        "tipo",
        "fecha",
        "origen_nombre",
        "origen_identificacion",
    )

    list_filter = (
        "tipo",
        "fecha",
    )

    search_fields = (
        "animal__numero_arete",
        "animal__nombre_propio",
        "origen_nombre",
        "origen_identificacion",
    )

    autocomplete_fields = (
        "animal",
    )


# ============================================================
# COMPOSICIÓN GENÉTICA
# ============================================================

@admin.register(ComposicionGenetica)
class ComposicionGeneticaAdmin(admin.ModelAdmin):

    list_display = (
        "animal",
        "raza",
        "porcentaje",
        "metodo",
        "confiabilidad",
        "fecha_verificacion",
    )

    list_filter = (
        "metodo",
        "confiabilidad",
        "raza",
    )

    search_fields = (
        "animal__numero_arete",
        "animal__nombre_propio",
        "raza__nombre",
    )

    autocomplete_fields = (
        "animal",
        "raza",
    )

    ordering = (
        "animal",
        "-porcentaje",
    )


# ============================================================
# DOCUMENTOS
# ============================================================

@admin.register(DocumentoAnimal)
class DocumentoAnimalAdmin(admin.ModelAdmin):

    list_display = (
        "animal",
        "tipo",
        "numero_documento",
        "fecha_documento",
    )

    list_filter = (
        "tipo",
        "fecha_documento",
    )

    search_fields = (
        "animal__numero_arete",
        "animal__nombre_propio",
        "numero_documento",
    )

    autocomplete_fields = (
        "animal",
    )

    date_hierarchy = "fecha_documento"


# ============================================================
# MOVIMIENTOS
# ============================================================

@admin.register(MovimientoAnimal)
class MovimientoAnimalAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "animal",
        "potrero",
        "tipo_pasto",
        "fecha_entrada",
        "fecha_salida",
        "activo",
    )

    list_filter = (
        "potrero",
        "tipo_pasto",
        "activo",
        "fecha_entrada",
    )

    search_fields = (
        "animal__numero_arete",
        "animal__nombre_propio",
    )

    autocomplete_fields = (
        "animal",
        "potrero",
        "tipo_pasto",
    )

    date_hierarchy = "fecha_entrada"

    ordering = (
        "-fecha_entrada",
    )


# ============================================================
# PESAJE
# ============================================================

@admin.register(PesajeAnimal)
class PesajeAnimalAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "animal",
        "fecha",
        "peso_kg",
    )

    list_filter = (
        "fecha",
    )

    search_fields = (
        "animal__numero_arete",
        "animal__nombre_propio",
    )

    autocomplete_fields = (
        "animal",
    )

    date_hierarchy = "fecha"

    ordering = (
        "-fecha",
    )


# ============================================================
# EVENTO DE SALUD
# ============================================================

@admin.register(EventoSalud)
class EventoSaludAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "animal",
        "tipo",
        "fecha",
        "producto",
        "dosis",
        "nombre_veterinario",
    )

    list_filter = (
        "tipo",
        "fecha",
    )

    search_fields = (
        "animal__numero_arete",
        "animal__nombre_propio",
        "producto",
        "nombre_veterinario",
    )

    autocomplete_fields = (
        "animal",
    )

    date_hierarchy = "fecha"

    ordering = (
        "-fecha",
    )
