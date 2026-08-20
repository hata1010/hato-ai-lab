from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from django.core.exceptions import PermissionDenied

from .models import Finca, Potrero, UsuarioFinca
from apps.ganado.models import MovimientoAnimal
from apps.core.tenant import obtener_fincas_usuario


# ============================================================
# UTILIDADES DE AUTORIZACIÓN
# ============================================================

def usuario_es_superusuario(request):
    """Determina si el usuario actual es superusuario."""
    return (
        request.user.is_authenticated
        and request.user.is_superuser
    )


def usuario_puede_acceder_finca(request, finca):
    """
    Determina si el usuario puede acceder a una finca.

    El superusuario tiene acceso global.
    Los demás usuarios dependen de UsuarioFinca.
    """
    if usuario_es_superusuario(request):
        return True

    if finca is None:
        return False

    return finca.usuarios_autorizados.filter(
        usuario=request.user,
        activa=True,
    ).exists()


# ============================================================
# INLINE: POTREROS DENTRO DE LA FINCA
# ============================================================

class PotreroInline(admin.TabularInline):

    model = Potrero

    extra = 0

    can_delete = True

    fields = (
        'nombre',
        'codigo',
        'tipo',
        'estado',
        'area_hectareas',
        'poligono',
    )

    readonly_fields = (
        'area_hectareas',
    )

    def has_add_permission(self, request, obj=None):
        """
        Permite agregar potreros únicamente si:

        - el usuario es superusuario, o
        - el usuario tiene acceso activo a la finca.
        """
        if usuario_es_superusuario(request):
            return True

        if obj is None:
            return False

        return usuario_puede_acceder_finca(request, obj)

    def has_change_permission(self, request, obj=None):
        """
        Permite modificar potreros solamente dentro
        de una finca autorizada.
        """
        if usuario_es_superusuario(request):
            return True

        if obj is None:
            return True

        return usuario_puede_acceder_finca(request, obj)

    def has_delete_permission(self, request, obj=None):
        """
        Permite eliminar potreros solamente dentro
        de una finca autorizada.
        """
        if usuario_es_superusuario(request):
            return True

        if obj is None:
            return True

        return usuario_puede_acceder_finca(request, obj)


# ============================================================
# INLINE: ANIMALES ACTIVOS DENTRO DEL POTRERO
# ============================================================

class AnimalesEnPotreroInline(admin.TabularInline):

    model = MovimientoAnimal

    extra = 0

    can_delete = False

    readonly_fields = (
        'animal',
        'fecha_entrada',
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .filter(activo=True)
        )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# ============================================================
# ADMINISTRACIÓN DE FINCAS
# ============================================================

@admin.register(Finca)
class FincaAdmin(GISModelAdmin):

    list_display = (
        'id',
        'nombre',
        'nit',
        'ubicacion',
        'area_total',
        'is_active',
    )

    list_filter = (
        'is_active',
        'zona_horaria',
        'moneda',
    )

    search_fields = (
        'nombre',
        'nit',
        'direccion',
        'email',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    # ========================================================
    # Potreros administrados directamente desde la finca
    # ========================================================

    inlines = [
        PotreroInline,
    ]

    # ========================================================
    # FILTRO PRINCIPAL DE FINCAS
    # ========================================================

    def get_queryset(self, request):
        """
        Superusuario:
            ve todas las fincas.

        Usuario normal:
            solamente ve las fincas que tenga asignadas
            mediante UsuarioFinca y cuya membresía esté activa.
        """

        queryset = super().get_queryset(request)

        if usuario_es_superusuario(request):
            return queryset

        return queryset.filter(
            usuarios_autorizados__usuario=request.user,
            usuarios_autorizados__activa=True,
            is_active=True,
        ).distinct()

    # ========================================================
    # PERMISOS DE VISUALIZACIÓN
    # ========================================================

    def has_view_permission(self, request, obj=None):

        if not request.user.is_authenticated:
            return False

        if usuario_es_superusuario(request):
            return True

        if obj is None:
            return True

        return usuario_puede_acceder_finca(request, obj)

    # ========================================================
    # PERMISOS DE MODIFICACIÓN
    # ========================================================

    def has_change_permission(self, request, obj=None):
       if usuario_es_superusuario(request):
        return True

        if obj is None:
            return True

        return usuario_puede_acceder_finca(request, obj)

    # ========================================================
    # CREACIÓN DE FINCAS
    # ========================================================

    def has_add_permission(self, request):

        """
        Las fincas nuevas son creadas únicamente por
        el superusuario.

        Un usuario normal primero recibe una finca mediante
        UsuarioFinca.
        """

        return usuario_es_superusuario(request)

    # ========================================================
    # ELIMINACIÓN DE FINCAS
    # ========================================================

    def has_delete_permission(self, request, obj=None):

        if usuario_es_superusuario(request):
            return True

        return False

    # ========================================================
    # FIELDSETS
    # ========================================================

    fieldsets = (
        (
            'Información General',
            {
                'fields': (
                    'nombre',
                    'nit',
                    'direccion',
                    'telefono',
                    'email',
                    'ubicacion',
                )
            },
        ),
        (
            'Datos de la Finca',
            {
                'fields': (
                    'area_total',
                    'fecha_fundacion',
                    'zona_horaria',
                    'moneda',
                    'descripcion',
                )
            },
        ),
        (
            'Auditoría',
            {
                'fields': (
                    'is_active',
                    'created_by',
                    'created_at',
                    'updated_at',
                )
            },
        ),
    )


# ============================================================
# ADMINISTRACIÓN DE POTREROS
# ============================================================

@admin.register(Potrero)
class PotreroAdmin(GISModelAdmin):

    list_display = (
        'id',
        'nombre',
        'finca',
        'codigo',
        'tipo',
        'ubicacion',
        'estado',
        'area_hectareas',
    )

    list_filter = (
        'tipo',
        'estado',
        'calidad_pasto',
        'is_active',
        'finca',
    )

    search_fields = (
        'nombre',
        'codigo',
        'descripcion',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'area_hectareas',
    )

    # ========================================================
    # Animales activos dentro del potrero
    # ========================================================

    inlines = [
        AnimalesEnPotreroInline,
    ]

    # ========================================================
    # FILTRO DE POTREROS
    # ========================================================

    def get_queryset(self, request):

        queryset = super().get_queryset(request)

        if usuario_es_superusuario(request):
            return queryset

        return queryset.filter(
            finca__usuarios_autorizados__usuario=request.user,
            finca__usuarios_autorizados__activa=True,
            finca__is_active=True,
        ).distinct()

    # ========================================================
    # PERMISOS DE VISUALIZACIÓN
    # ========================================================

    def has_view_permission(self, request, obj=None):

        if not request.user.is_authenticated:
            return False

        if usuario_es_superusuario(request):
            return True

        if obj is None:
            return True

        return usuario_puede_acceder_finca(
            request,
            obj.finca, 
        )

    # ========================================================
    # PERMISOS DE MODIFICACIÓN
    # ========================================================

    def has_change_permission(self, request, obj=None):

        if usuario_es_superusuario(request):
            return True

        if obj is None:
            return True

        return usuario_puede_acceder_finca(
            request,
            obj.finca,
        )

    # ========================================================
    # CREACIÓN
    # ========================================================

    def has_add_permission(self, request):

        if usuario_es_superusuario(request):
            return True

        return obtener_fincas_usuario(request.user).exists()

    # ========================================================
    # ELIMINACIÓN
    # ========================================================

    def has_delete_permission(self, request, obj=None):

        if usuario_es_superusuario(request):
            return True

        if obj is None:
            return True

        return usuario_puede_acceder_finca(
            request,
            obj.finca,
        )

    # ========================================================
    # LIMITAR EL CAMPO FINCA
    # ========================================================

    def formfield_for_foreignkey(
        self,
        db_field,
        request,
        **kwargs,
    ):
        """
        Cuando un usuario normal crea un potrero,
        solamente puede seleccionar fincas que tenga
        asignadas mediante UsuarioFinca.
        """

        if db_field.name == 'finca':

            if usuario_es_superusuario(request):

                kwargs['queryset'] = Finca.objects.filter(
                    is_active=True,
                )

            else:

                kwargs['queryset'] = obtener_fincas_usuario(
                    request.user,
                )

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs,
        )

    # ========================================================
    # SEGURIDAD ADICIONAL AL GUARDAR
    # ========================================================

    def save_model(
        self,
        request,
        obj,
        form,
        change,
    ):
        """
        Segunda barrera de seguridad.

        Aunque alguien manipule el formulario,
        no puede guardar un potrero en una finca
        que no tenga autorizada.
        """

        if not usuario_es_superusuario(request):

            if not usuario_puede_acceder_finca(
                request,
                obj.finca,
            ):
                raise PermissionDenied(
                    "No tienes autorización para "
                    "administrar esta finca."
                )

        super().save_model(
            request,
            obj,
            form,
            change,
        )

    # ========================================================
    # FIELDSETS
    # ========================================================

    fieldsets = (
        (
            'Datos Generales',
            {
                'fields': (
                    'finca',
                    'nombre',
                    'codigo',
                    'tipo',
                    'ubicacion',
                )
            },
        ),
        (
            'Datos del Terreno',
            {
                'fields': (
                    'capacidad_animales',
                    'carga_actual',
                    'poligono',
                )
            },
        ),
        (
            'Información del Pasto',
            {
                'fields': (
                    'tipo_pasto',
                    'calidad_pasto',
                )
            },
        ),
        (
            'Estado y Rotación',
            {
                'fields': (
                    'estado',
                    'dias_descanso',
                    'fecha_ultimo_pastoreo',
                )
            },
        ),
        (
            'Área calculada por el sistema',
            {
                'fields': (
                    'area_hectareas',
                )
            },
        ),
        (
            'Otros',
            {
                'fields': (
                    'descripcion',
                    'is_active',
                    'created_at',
                    'updated_at',
                )
            },
        ),
    )


# ============================================================
# ADMINISTRACIÓN DE USUARIOS POR FINCA
#
# Relación:
#
# Usuario Django
#       ↓
# UsuarioFinca
#       ↓
#      Finca
#
# Esta tabla determina qué usuario puede acceder
# a qué finca y con qué rol.
# ============================================================

@admin.register(UsuarioFinca)
class UsuarioFincaAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'usuario',
        'finca',
        'rol',
        'activa',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'activa',
        'rol',
        'finca',
    )

    search_fields = (
        'usuario__username',
        'usuario__first_name',
        'usuario__last_name',
        'usuario__email',
        'finca__nombre',
        'finca__nit',
    )

    autocomplete_fields = (
        'usuario',
        'finca',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        (
            'Asignación de acceso',
            {
                'fields': (
                    'usuario',
                    'finca',
                    'rol',
                    'activa',
                )
            },
        ),
        (
            'Auditoría',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                )
            },
        ),
    )

    ordering = (
        'finca',
        'usuario',
    )

    # ========================================================
    # LISTADO DE MEMBRESÍAS
    # ========================================================

    def get_queryset(self, request):

        queryset = super().get_queryset(request)

        if usuario_es_superusuario(request):
            return queryset

        # Un usuario normal solamente puede ver
        # sus propias membresías.
        return queryset.filter(
            usuario=request.user,
            activa=True,
        )

    # ========================================================
    # VISUALIZACIÓN
    # ========================================================

    def has_view_permission(self, request, obj=None):

        if not request.user.is_authenticated:
            return False

        if usuario_es_superusuario(request):
            return True

        if obj is None:
            return True

        return (
            obj.usuario_id == request.user.id
            and obj.activa
        )

    # ========================================================
    # CREACIÓN
    # ========================================================

    def has_add_permission(self, request):

        """
        Solamente el superusuario puede asignar
        usuarios a fincas.
        """

        return usuario_es_superusuario(request)

    # ========================================================
    # MODIFICACIÓN
    # ========================================================

    def has_change_permission(self, request, obj=None):

        return usuario_es_superusuario(request)

    # ========================================================
    # ELIMINACIÓN
    # ========================================================

    def has_delete_permission(self, request, obj=None):

        return usuario_es_superusuario(request)