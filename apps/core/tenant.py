"""Módulo de gestión de Tenant y Contexto de Finca Activa para Hato V1."""

from typing import Any, Optional


def _get_models():
    """
    Importación diferida de los modelos para evitar problemas
    de importación circular.
    """
    from apps.core.models import Finca, UsuarioFinca

    return Finca, UsuarioFinca


def obtener_fincas_usuario(user):
    """
    Retorna el queryset de fincas a las que el usuario
    tiene acceso legítimo.

    Superusuario:
        Puede acceder a todas las fincas activas.

    Usuario normal:
        Solo puede acceder a las fincas donde existe una
        membresía UsuarioFinca activa.
    """

    if not user or not getattr(user, "is_authenticated", False):
        return []

    Finca, UsuarioFinca = _get_models()

    # --------------------------------------------------------
    # SUPERUSUARIO
    # --------------------------------------------------------
    if getattr(user, "is_superuser", False):
        return Finca.objects.filter(
            is_active=True
        )

    # --------------------------------------------------------
    # USUARIO NORMAL
    # --------------------------------------------------------
    return Finca.objects.filter(
        usuarios_autorizados__usuario=user,
        usuarios_autorizados__activa=True,
        is_active=True,
    ).distinct()


def verificar_acceso_finca(user, finca) -> bool:
    """
    Verifica si un usuario tiene autorización para operar
    sobre una finca específica.
    """

    if (
        not user
        or not getattr(user, "is_authenticated", False)
        or finca is None
    ):
        return False

    # --------------------------------------------------------
    # SUPERUSUARIO
    # --------------------------------------------------------
    if getattr(user, "is_superuser", False):
        return True

    # --------------------------------------------------------
    # USUARIO NORMAL
    # --------------------------------------------------------
    _, UsuarioFinca = _get_models()

    return UsuarioFinca.objects.filter(
        usuario=user,
        finca=finca,
        activa=True,
    ).exists()


def obtener_rol_usuario_finca(
    user,
    finca
) -> Optional[str]:
    """
    Retorna el rol que tiene el usuario dentro de una finca.

    Valores posibles definidos por UsuarioFinca:
        propietario
        administrador
        operador
        veterinario
        auditor
    """

    if (
        not user
        or not getattr(user, "is_authenticated", False)
        or finca is None
    ):
        return None

    # --------------------------------------------------------
    # SUPERUSUARIO
    # --------------------------------------------------------
    if getattr(user, "is_superuser", False):
        return "superusuario"

    # --------------------------------------------------------
    # USUARIO NORMAL
    # --------------------------------------------------------
    _, UsuarioFinca = _get_models()

    membresia = (
        UsuarioFinca.objects
        .filter(
            usuario=user,
            finca=finca,
            activa=True,
        )
        .first()
    )

    return membresia.rol if membresia else None


def obtener_finca_activa(request):
    """
    Resuelve la finca activa para la sesión actual del usuario.

    Prioridad:

    1. Superusuario + finca seleccionada en sesión.
    2. Usuario normal + finca autorizada seleccionada en sesión.
    3. Primera finca autorizada.
    """

    user = getattr(request, "user", None)

    if (
        not user
        or not getattr(user, "is_authenticated", False)
    ):
        return None

    Finca, _ = _get_models()

    session = getattr(request, "session", {})

    finca_sesion_id = session.get(
        "finca_activa_id"
    )

    # ========================================================
    # SUPERUSUARIO
    # ========================================================

    if getattr(user, "is_superuser", False):

        # ----------------------------------------------------
        # Intentar recuperar la finca seleccionada
        # ----------------------------------------------------
        if finca_sesion_id:

            finca = (
                Finca.objects
                .filter(
                    id=finca_sesion_id,
                    is_active=True,
                )
                .first()
            )

            if finca:
                return finca

        # ----------------------------------------------------
        # Si no hay finca seleccionada, usar la primera activa
        # ----------------------------------------------------
        return (
            Finca.objects
            .filter(is_active=True)
            .first()
        )

    # ========================================================
    # USUARIO NORMAL
    # ========================================================

    fincas_autorizadas = obtener_fincas_usuario(user)

    if not fincas_autorizadas.exists():
        return None

    # --------------------------------------------------------
    # Intentar recuperar finca almacenada en sesión
    # --------------------------------------------------------

    if finca_sesion_id:

        finca = (
            fincas_autorizadas
            .filter(id=finca_sesion_id)
            .first()
        )

        if finca:
            return finca

    # --------------------------------------------------------
    # AUTO-SELECCIÓN
    # --------------------------------------------------------

    primera_finca = fincas_autorizadas.first()

    if (
        primera_finca
        and hasattr(request, "session")
    ):
        request.session["finca_activa_id"] = (
            primera_finca.id
        )

    return primera_finca


def cambiar_finca_activa(
    request,
    finca_id: Any
):
    """
    Cambia la finca activa previa validación de autorización.

    Si el usuario intenta seleccionar una finca a la que
    no tiene acceso, se genera HTTP 403 mediante PermissionDenied.
    """

    from django.core.exceptions import PermissionDenied

    Finca, _ = _get_models()

    user = getattr(request, "user", None)

    # ========================================================
    # AUTENTICACIÓN
    # ========================================================

    if (
        not user
        or not getattr(user, "is_authenticated", False)
    ):
        raise PermissionDenied(
            "Debe iniciar sesión para seleccionar una finca."
        )

    # ========================================================
    # VALIDAR ID
    # ========================================================

    try:
        finca_id_int = int(finca_id)

    except (TypeError, ValueError):

        raise PermissionDenied(
            "Identificador de finca inválido."
        )

    # ========================================================
    # BUSCAR FINCA ACTIVA
    # ========================================================

    finca = (
        Finca.objects
        .filter(
            id=finca_id_int,
            is_active=True,
        )
        .first()
    )

    if not finca:

        raise PermissionDenied(
            "La finca solicitada no existe o está inactiva."
        )

    # ========================================================
    # VALIDAR AUTORIZACIÓN
    # ========================================================

    if not verificar_acceso_finca(
        user,
        finca
    ):

        raise PermissionDenied(
            "No tienes autorización para acceder a esta finca."
        )

    # ========================================================
    # GUARDAR FINCA ACTIVA EN LA SESIÓN
    # ========================================================

    if hasattr(request, "session"):

        request.session["finca_activa_id"] = (
            finca.id
        )

        # Garantiza que Django persista la modificación
        request.session.modified = True

    return finca