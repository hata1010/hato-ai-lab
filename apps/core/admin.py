from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import Finca, Potrero
from apps.ganado.models import MovimientoAnimal

# ============================================================
# NUEVO INLINE: Potreros dentro de la Finca
# ============================================================
class PotreroInline(admin.TabularInline):
    model = Potrero
    extra = 0  # No muestra filas vacías por defecto
    can_delete = True
    fields = ('nombre', 'codigo', 'tipo', 'estado', 'area_hectareas', 'poligono')
    readonly_fields = ('area_hectareas',)


# ============================================================
# INLINE: Muestra los animales activos dentro de cada potrero
# ============================================================
class AnimalesEnPotreroInline(admin.TabularInline):
    model = MovimientoAnimal
    extra = 0
    can_delete = False
    readonly_fields = ('animal', 'fecha_entrada')
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(activo=True)
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Finca)
class FincaAdmin(GISModelAdmin):
    list_display = ('id', 'nombre', 'nit', 'ubicacion', 'area_total', 'is_active')
    list_filter = ('is_active', 'zona_horaria', 'moneda')
    search_fields = ('nombre', 'nit', 'direccion', 'email')
    readonly_fields = ('created_at', 'updated_at')
    
    # AQUÍ AGREGAMOS EL INLINE DE POTREROS
    inlines = [PotreroInline]
    
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'nit', 'direccion', 'telefono', 'email', 'ubicacion')
        }),
        ('Datos de la Finca', {
            'fields': ('area_total', 'fecha_fundacion', 'zona_horaria', 'moneda', 'descripcion')
        }),
        ('Auditoría', {
            'fields': ('is_active', 'created_by', 'created_at', 'updated_at')
        }),
    )


@admin.register(Potrero)
class PotreroAdmin(GISModelAdmin):
    list_display = ('id', 'nombre', 'finca', 'codigo', 'tipo', 'ubicacion', 'estado', 'area_hectareas')
    list_filter = ('tipo', 'estado', 'calidad_pasto', 'is_active', 'finca')
    search_fields = ('nombre', 'codigo', 'descripcion')
    readonly_fields = ('created_at', 'updated_at', 'area_hectareas')
    
    inlines = [AnimalesEnPotreroInline]
    
    fieldsets = (
        ('Datos Generales', {
            'fields': ('finca', 'nombre', 'codigo', 'tipo', 'ubicacion')
        }),
        ('Datos del Terreno', {
            'fields': ('capacidad_animales', 'carga_actual', 'poligono')
        }),
        ('Información del Pasto', {
            'fields': ('tipo_pasto', 'calidad_pasto')
        }),
        ('Estado y Rotación', {
            'fields': ('estado', 'dias_descanso', 'fecha_ultimo_pastoreo')
        }),
        ('Área calculada por el sistema', {
            'fields': ('area_hectareas',)
        }),
        ('Otros', {
            'fields': ('descripcion', 'is_active', 'created_at', 'updated_at')
        }),
    )